"""FIS Pipeline — processes files into classification cards.

Flow:
  1. Baseline rename (mechanical, no NLP)
  2. Extract text
  3. YAKE keywords (always)
  4. spaCy entities (always)
  5. Domain classification (DeBERTa zero-shot or rule-based fallback)
  6. File type meaning (DeBERTa zero-shot or rule-based fallback)
  7. Summary (BART abstractive or extractive fallback)
  8. Build slug from keywords
  9. Generate rename presets
  10. Assemble classification card
  11. Write .fcard manifest
"""
import json
import logging
from pathlib import Path
from datetime import datetime

from fis.baseline import to_baseline, to_slug, build_rename_preview
from fis.extractor import extract_text, SKIP_EXTENSIONS
from fis.card import build_card, write_manifest
from fis.db import insert_card

logger = logging.getLogger("fis")


class FISPipeline:
    """Main FIS processing pipeline."""

    def __init__(self, use_bart: bool = True, use_deberta: bool = True,
                 config_path: str = None):
        # Load config
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        with open(config_path) as f:
            self.config = json.load(f)

        cfg = self.config
        pipe_cfg = cfg.get("pipeline", {})
        self.max_tags = pipe_cfg.get("max_tags", 5)
        self.max_keywords = pipe_cfg.get("max_keywords", 6)
        self.slug_max = pipe_cfg.get("slug_max_chars", 50)
        self.summary_max_words = pipe_cfg.get("summary_max_words", 30)
        self.review_threshold = pipe_cfg.get("confidence_review_threshold", 50)
        self.domains = cfg.get("domains", [])
        self.file_types = cfg.get("file_type_meanings", [])

        # Always-on engines
        from fis.engines import YakeEngine, SpacyEngine
        self.yake = YakeEngine(top_n=pipe_cfg.get("yake_top_n", 10))
        self.spacy = SpacyEngine(cfg.get("models", {}).get("spacy_model", "en_core_web_sm"))

        # Optional heavy engines (lazy load)
        self._deberta = None
        self._bart = None
        self.use_bart = use_bart and cfg.get("models", {}).get("use_bart", True)
        self.use_deberta = use_deberta and cfg.get("models", {}).get("use_deberta", True)

    def _get_deberta(self):
        if self._deberta is None:
            from fis.engines import DeBERTaClassifier
            path = self.config["models"]["deberta_path"]
            logger.info(f"Loading DeBERTa from {path}")
            self._deberta = DeBERTaClassifier(path)
        return self._deberta

    def _get_bart(self):
        if self._bart is None:
            from fis.engines import BARTSummarizer
            path = self.config["models"]["bart_path"]
            logger.info(f"Loading BART from {path}")
            self._bart = BARTSummarizer(path)
        return self._bart

    def process_file(self, file_path: Path) -> dict:
        """Process a single file into a classification card."""
        ext = file_path.suffix.lower()

        # Step 1: Baseline rename (mechanical)
        baseline = to_baseline(file_path.name)

        # Step 2: Extract text
        text = extract_text(file_path)
        if not text.strip():
            # Can't classify — return minimal card
            return build_card(
                file_path=file_path, baseline=baseline,
                domain="unknown", domain_confidence=0,
                file_type_meaning="unknown", file_type_confidence=0,
                summary="No text content could be extracted.",
                tags=[], keywords=[], slug=baseline.rsplit('.', 1)[0],
                rename_preview={"baseline": baseline, "presets": {}},
                confidence_threshold=self.review_threshold,
            )

        # Step 3: YAKE keywords
        yake_results = self.yake.extract(text)
        keywords = [r["keyword"] for r in yake_results[:self.max_keywords]]

        # Step 4: spaCy entities
        entities = self.spacy.extract(text)
        entity_tags = list({e["entity"].lower() for e in entities})[:3]

        # Step 5+6: Domain + file_type_meaning
        if self.use_deberta:
            deberta = self._get_deberta()
            domain_result = deberta.classify(text, self.domains)
            type_result = deberta.classify(text, self.file_types)
            domain = domain_result["label"]
            domain_conf = domain_result["confidence"]
            file_type = type_result["label"]
            type_conf = type_result["confidence"]
        else:
            from fis.engines import rule_based_classify
            rb = rule_based_classify(text, yake_results)
            domain = rb["domain"]
            domain_conf = rb["domain_confidence"]
            file_type = rb["file_type_meaning"]
            type_conf = rb["file_type_confidence"]

        # Step 7: Summary
        if self.use_bart:
            summary = self._get_bart().summarize(text, self.summary_max_words)
        else:
            from fis.engines import extractive_summary
            summary = extractive_summary(text)

        # Step 8: Slug
        slug = to_slug(keywords[:4], self.slug_max)

        # Step 9: Tags (blend YAKE top keywords + entity tags)
        kw_tags = [k.lower().replace(' ', '_') for k in keywords[:3]]
        tags = list(dict.fromkeys(kw_tags + entity_tags + [domain]))[:self.max_tags]

        # Step 10: Rename preview
        rename_preview = build_rename_preview(
            domain=domain, keywords=keywords, file_type=file_type,
            slug=slug, ext=ext,
        )

        # Step 11: Build card
        card = build_card(
            file_path=file_path, baseline=baseline,
            domain=domain, domain_confidence=domain_conf,
            file_type_meaning=file_type, file_type_confidence=type_conf,
            summary=summary, tags=tags, keywords=keywords, slug=slug,
            rename_preview=rename_preview,
            confidence_threshold=self.review_threshold,
        )

        # Step 12: Persist to shared FIS database
        try:
            insert_card(card)
        except Exception as e:
            logger.warning(f"DB insert failed (card still valid): {e}")

        return card

    def process_folder(self, folder_path: Path) -> list[dict]:
        """Process all files in a folder into classification cards."""
        cards = []
        for item in sorted(folder_path.iterdir()):
            if item.is_dir():
                continue
            if item.suffix.lower() in SKIP_EXTENSIONS:
                continue
            if item.name.startswith('.') or item.name.startswith('_manifest'):
                continue
            try:
                card = self.process_file(item)
                cards.append(card)
                logger.info(f"Classified: {item.name} -> {card['domain']['value']}")
            except Exception as e:
                logger.error(f"Failed: {item.name}: {e}")
        return cards

    def write_manifest(self, cards: list[dict], folder_path: Path) -> Path:
        """Write cards to .fcard manifest in the folder."""
        return write_manifest(cards, folder_path)
