# Backside Station Output Inventory

Date: 2026-05-24

- Registry root: `X:\Backside\workflows\knowledge-refinery.workflow\BACKSIDE\STATIONS\stations`
- Live stations inventoried: `64`
- Source of truth: each station `station.yml`, specifically `output.produces` and `output.required_format`.

## Quick Pattern Summary

- `55` station(s): `result.json`, `result.md`
- `1` station(s): `claims.json`, `claims.md`
- `1` station(s): `conversion_report.yml`, `source.md`
- `1` station(s): `evidence_7q.json`, `evidence_7q.md`
- `1` station(s): `forward_7q.json`, `forward_7q.md`
- `1` station(s): `graph.json`, `graph.md`
- `1` station(s): `publication_status.yml`, `release_recommendation.md`
- `1` station(s): `reverse_7q.json`, `reverse_7q.md`
- `1` station(s): `routing.yml`, `routing.md`
- `1` station(s): `summary.lossless.json`, `summary.lossless.md`

## Per Station

| Order | Station ID | Folder | Lane | Name | Output Files | Format | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ST-EMBED-001` | `sci_embed` | `embed` | Sci Embed | `result.json`<br>`result.md` | `json` | Embed scientific papers using SPECTER2 for similarity, dedup, and retrieval. |
| 2 | `ST-TIME-001` | `timeline` | `time` | Timeline | `result.json`<br>`result.md` | `json` | Extract temporal information (dates, durations, ordering) from text. Stub until David provides recipe. |
| 3 | `ST-NLI-001` | `nli_strong` | `nli` | NLI Strong | `result.json`<br>`result.md` | `json` | Strong NLI via DeBERTa v3 large — entailment / contradiction / neutral on premise+hypothesis pairs. |
| 4 | `ST-NLI-002` | `nli_claim` | `nli` | NLI Claim | `result.json`<br>`result.md` | `json` | Claim-verification NLI tuned on MNLI/FEVER/ANLI for fact-checking pipelines. |
| 5 | `ST-NLI-003` | `nli_alt` | `nli` | NLI Alt (RoBERTa) | `result.json`<br>`result.md` | `json` | Secondary NLI (RoBERTa large) for adversarial cross-check against the strong NLI. |
| 6 | `ST-EMBED-002` | `embed_general` | `embed` | Embed General (MiniLM) | `result.json`<br>`result.md` | `json` | General sentence embeddings (MiniLM) for dedup, routing, and quick similarity. |
| 7 | `ST-NLI-004` | `nli_base` | `nli` | NLI Base (legacy) | `result.json`<br>`result.md` | `json` | Baseline NLI (legacy) — kept as fallback / regression baseline. |
| 8 | `ST-RERANK-001` | `rerank` | `rerank` | Rerank (cross-encoder) | `result.json`<br>`result.md` | `json` | Cross-encoder reranker — score (query, passage) pairs for retrieval ranking. |
| 9 | `ST-SEVENQ-001` | `7q_forward` | `sevenq` | 7Q Forward (classification) | `forward_7q.json`<br>`forward_7q.md` | `json` | Forward 7-Question Scientific Method — classification pass on a paper (Q0..Q7). What is this paper saying? |
| 10 | `ST-SEVENQ-002` | `7q_reverse` | `sevenq` | 7Q Reverse (kill test) | `reverse_7q.json`<br>`reverse_7q.md` | `json` | Reverse 7-Question Scientific Method — adversarial kill test (R1..R7). Find the weakest link, test if the claim survives. |
| 11 | `ST-SEVENQ-003` | `7q_evidence` | `sevenq` | 7Q Evidence (pressure) | `evidence_7q.json`<br>`evidence_7q.md` | `json` | Evidence pressure pass — classify evidence as direct / indirect / analogical / weak / conflicting; identify gaps; prepare citation targets. |
| 12 | `ST-CONV-012` | `html_to_md` | `conv` | Html To Md | `result.json`<br>`result.md` | `json` | Convert HTML to clean Markdown via MarkItDown. |
| 12 | `ST-7QS-012` | `reasoning_worker` | `7qs` | Reasoning Worker | `result.json`<br>`result.md` | `json` | General reasoning worker for 7QS + station decisions. |
| 12 | `ST-ROUTE-001` | `route_classifier` | `route` | Route Classifier | `routing.yml`<br>`routing.md` | `json` | Inspect a dropped file, detect type (PDF/HTML/MD/DOCX/transcript/audio/video/JSON), assign workflow lane, produce routing.yml. |
| 13 | `ST-CODE-013` | `code_worker` | `code` | Code Worker | `result.json`<br>`result.md` | `json` | Code/script worker for station script generation and repair. |
| 13 | `ST-CONV-001` | `document_converter` | `conv` | Route Conversion Dispatcher | `conversion_report.yml`<br>`source.md` | `json` | Sniff incoming file type (extension + magika content classification) and route to the appropriate downstream CONV station (ST-CONV-012..026). This station does NOT convert — it only dispatches. MarkItDown, Docling, and Marker are BACKENDS used inside the granular stations, not stations themselves. |
| 13 | `ST-CONV-013` | `pdf_to_md` | `conv` | Pdf To Md | `result.json`<br>`result.md` | `json` | Convert text-selectable PDF to Markdown via Docling (do_ocr=False). |
| 14 | `ST-CLAIM-001` | `claim_extractor` | `claim` | Claim Extractor | `claims.json`<br>`claims.md` | `json` | Read source.md, extract durable claims, assumptions, equations, hypotheses, evidence statements. Assign claim IDs. Dedup against existing claim store. |
| 14 | `ST-CONV-014` | `docx_to_md` | `conv` | Docx To Md | `result.json`<br>`result.md` | `json` | Convert DOCX to Markdown via MarkItDown. |
| 14 | `ST-LCTX-014` | `longctx_worker` | `lctx` | Longctx Worker | `result.json`<br>`result.md` | `json` | Long-context lossless worker for big papers/chats. |
| 15 | `ST-SUM-001` | `lossless_summary` | `sum` | Lossless Summary | `summary.lossless.json`<br>`summary.lossless.md` | `json` | Preserve the argument without flattening it — keeps claims, evidence, equations, assumptions, argument order, unresolved gaps. NOT a short summary. |
| 15 | `ST-CITE-015` | `paperqa2_literature` | `cite` | Paperqa2 Literature | `result.json`<br>`result.md` | `json` | Literature/citation retrieval agent wrapper. |
| 15 | `ST-CONV-015` | `pptx_to_md` | `conv` | Pptx To Md | `result.json`<br>`result.md` | `json` | Convert PPTX to Markdown via MarkItDown. |
| 16 | `ST-CONV-016` | `audio_to_txt` | `conv` | Audio To Txt | `result.json`<br>`result.md` | `json` | Transcribe audio file to plain text via faster-whisper (CPU). |
| 16 | `ST-GRAPH-001` | `knowledge_graph` | `graph` | Knowledge Graph | `graph.json`<br>`graph.md` | `json` | Turn paper + claims + 7Q outputs + evidence into graph nodes (paper, claim, axiom_candidate, evidence, equation, domain, objection) and edges (supports, contradicts, depends_on, derives_from, maps_to, cites). Export JSON/CSV for Neo4j. |
| 17 | `ST-PUB-001` | `publication_gate` | `pub` | Publication Gate | `publication_status.yml`<br>`release_recommendation.md` | `json` | Read all artifacts. Check readiness (claims extracted, summary exists, reverse pass survived, evidence gaps acceptable, graph built, contradictions resolved). Recommend destination: website / Substack / Zenodo / Proof Explorer / Obsidian Canon / Review / Archive. |
| 17 | `ST-CONV-017` | `video_to_txt` | `conv` | Video To Txt | `result.json`<br>`result.md` | `json` | Extract audio with ffmpeg and transcribe via faster-whisper. |
| 18 | `ST-GRAPH-018` | `knowledge_graph_extractor` | `graph` | Knowledge Graph Extractor | `result.json`<br>`result.md` | `json` | Extract nodes/edges and supports/contradicts/depends_on. |
| 18 | `ST-CONV-018` | `youtube_to_txt` | `conv` | Youtube To Txt | `result.json`<br>`result.md` | `json` | Pull YouTube audio/captions via yt-dlp and emit transcript text. |
| 19 | `ST-CONV-019` | `md_cleaner` | `conv` | Md Cleaner | `result.json`<br>`result.md` | `json` | Normalize Markdown — heading levels, nav/footer strip, dedupe, link repair. |
| 20 | `ST-CONV-020` | `md_to_plaintext` | `conv` | Md To Plaintext | `result.json`<br>`result.md` | `json` | Strip Markdown to plain UTF-8 text. |
| 21 | `ST-CONV-021` | `equation_extract` | `conv` | Equation Extract | `result.json`<br>`result.md` | `json` | Extract equations from converted document into canonical LaTeX/MathML form. |
| 22 | `ST-CONV-022` | `table_extract` | `conv` | Table Extract | `result.json`<br>`result.md` | `json` | Extract tables from converted document into canonical CSV + Markdown table forms. |
| 23 | `ST-CONV-023` | `image_extract` | `conv` | Image Extract | `result.json`<br>`result.md` | `json` | Extract images, save to assets/, rewrite Markdown image links. |
| 24 | `ST-CONV-024` | `ocr_scan` | `conv` | Ocr Scan | `result.json`<br>`result.md` | `json` | OCR scanned/image-only PDFs to Markdown via Marker. |
| 25 | `ST-CONV-025` | `frontmatter_builder` | `conv` | Frontmatter Builder | `result.json`<br>`result.md` | `json` | Inject canonical YAML frontmatter (source_path, sha256, conversion_tool, converted_at, lineage). |
| 26 | `ST-CONV-026` | `asset_packager` | `conv` | Asset Packager | `result.json`<br>`result.md` | `json` | Package assets into canonical /assets/{slug}/ tree and rewrite Markdown refs. |
| 27 | `ST-7QS-027` | `evidence_pressure` | `7qs` | Evidence Pressure | `result.json`<br>`result.md` | `json` | Evidence pressure pass: what evidence is missing, what queries to run, what would falsify. |
| 28 | `ST-RED-028` | `cross_output_contradiction` | `red` | Cross Output Contradiction | `result.json`<br>`result.md` | `json` | Cross-output contradiction scan over artifacts emitted by prior stations. |
| 29 | `ST-NLP-001` | `semantic_drift` | `nlp` | Semantic Drift | `result.json`<br>`result.md` | `json` | Measure semantic drift across sections: claim meaning shifts over time. |
| 30 | `ST-NLP-002` | `retention_pressure` | `nlp` | Retention Pressure | `result.json`<br>`result.md` | `json` | Measure hook strength / retention pressure: forward pull, novelty density, tension/resolution pacing. |
| 31 | `ST-NLP-003` | `tone_consistency` | `nlp` | Tone Consistency | `result.json`<br>`result.md` | `json` | Measure tone/voice consistency and confidence fluctuation across the document. |
| 32 | `ST-NLP-004` | `epistemic_integrity` | `nlp` | Epistemic Integrity | `result.json`<br>`result.md` | `json` | Detect overclaims, unsupported certainty, hedging appropriateness, speculative-without-flag. |
| 33 | `ST-NLP-005` | `compression_density` | `nlp` | Compression Density | `result.json`<br>`result.md` | `json` | Measure conceptual compression density per sentence/paragraph (too low=fluff, too high=unreadable). |
| 34 | `ST-NLP-006` | `cognitive_load_gradient` | `nlp` | Cognitive Load Gradient | `result.json`<br>`result.md` | `json` | Measure cognitive load gradient: ramp smoothness, wall paragraphs, complexity spikes. |
| 35 | `ST-NLP-007` | `narrative_momentum` | `nlp` | Narrative Momentum | `result.json`<br>`result.md` | `json` | Measure narrative momentum: movement vs static exposition; tension progression. |
| 36 | `ST-NLP-008` | `bridge_density` | `nlp` | Bridge Density | `result.json`<br>`result.md` | `json` | Measure cross-domain bridge density + structural vs analogical bridge ratio. |
| 37 | `ST-NLP-009` | `redundancy_compression` | `nlp` | Redundancy Compression | `result.json`<br>`result.md` | `json` | Measure redundancy: repeated claims/metaphors/structures; semantic duplication. |
| 38 | `ST-NLP-010` | `dependency_stability` | `nlp` | Dependency Stability | `result.json`<br>`result.md` | `json` | Measure concept dependency stability: undefined terms, introduced-too-late dependencies. |
| 39 | `ST-NLP-011` | `reader_projection` | `nlp` | Reader Projection | `result.json`<br>`result.md` | `json` | Estimate reader projection support: general reader vs skeptic vs theologian vs scientist vs academic. |
| 40 | `ST-NLP-012` | `novelty_gradient` | `nlp` | Novelty Gradient | `result.json`<br>`result.md` | `json` | Measure concept novelty gradient: novelty spikes and cognitive shock points. |
| 41 | `ST-NLP-013` | `argument_closure` | `nlp` | Argument Closure | `result.json`<br>`result.md` | `json` | Measure argument closure score: does the paper resolve tensions it introduced? |
| 42 | `ST-NLP-014` | `symbol_consistency` | `nlp` | Symbol Consistency | `result.json`<br>`result.md` | `json` | Check internal symbol/variable consistency: variable drift, reuse ambiguity, equation naming stability. |
| 43 | `ST-NLP-015` | `rhetorical_temperature` | `nlp` | Rhetorical Temperature | `result.json`<br>`result.md` | `json` | Measure rhetorical temperature: emotional escalation, aggressive/defensive spikes affecting credibility. |
| 44 | `ST-YAML-001` | `yaml_schema_validator` | `yaml` | Yaml Schema Validator | `result.json`<br>`result.md` | `json` | Validate frontmatter against Theophysics Master YAML Schema + layer activation rules. |
| 45 | `ST-FACTS-001` | `facts_card_builder` | `facts` | Facts Card Builder | `result.json`<br>`result.md` | `json` | Emit FACTS-format cards (claims/evidence/equations) as a required downstream artifact. |
| 46 | `ST-SCORE-001` | `rubric_claim_indexer` | `score` | Rubric Claim Indexer | `result.json`<br>`result.md` | `json` | Scoring step 1: claim indexer (extract + classify claims for scoring). |
| 47 | `ST-SCORE-002` | `rubric_sectional_coherence` | `score` | Rubric Sectional Coherence | `result.json`<br>`result.md` | `json` | Scoring step 2: sectional coherence (score each section by role + coherence). |
| 48 | `ST-SCORE-003` | `rubric_meta_synthesis` | `score` | Rubric Meta Synthesis | `result.json`<br>`result.md` | `json` | Scoring step 3: meta-synthesis (combine multi-run outputs into consensus). |
| 49 | `ST-PUB-002` | `rubric_lsdp_formatter` | `pub` | Rubric Lsdp Formatter | `result.json`<br>`result.md` | `json` | Scoring step 4: LSDP protocol formatter (publication-ready manifest). |
| 50 | `ST-SESSION-001` | `session_record_builder` | `session` | Session Record Builder | `result.json`<br>`result.md` | `json` | Emit AI_SESSION record artifact (Goal/Context/Outputs/Decisions/Tasks/Memory/Links). |
| 51 | `ST-AXIOM-001` | `axiom_match` | `axiom` | Axiom Match | `result.json`<br>`result.md` | `json` | Axiom match: read axioms from Postgres, embed once/cache, brute-force cosine vs incoming claim embeddings; emit top-k matches. |
| 52 | `ST-NLI-005` | `contradiction_scan` | `nli` | Contradiction Scan | `result.json`<br>`result.md` | `json` | Contradiction scan: read axioms from Postgres and run NLI(claim, axiom) across corpus; emit contradiction hits over threshold. |
| 53 | `ST-CONV-027` | `pdf_classifier` | `conv` | PDF Classifier | `result.json`<br>`result.md` | `json` | Open a PDF and decide whether it has selectable text (route to ST-CONV-013 pdf_to_md) or is image-only/scanned (route to ST-CONV-024 ocr_scan). Pre-dispatcher for the CONV dispatcher. Dumb-layer: no reasoning, just character-density sampling. |
