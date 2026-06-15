"""
Run the full L1-L7 pipeline on ALL Convergence TX 6.6 papers.
Skips meta files (indexes, audits, excalidraw, pipeline pointers).
Outputs: Excel + JSON + L7 knowledge graph + per-paper vault-ready markdown.
"""
import sys, json, hashlib, re
from pathlib import Path
from datetime import datetime

# Re-use the orchestrator's machinery
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_pipeline import (
    analyze_paper, write_excel, _slugify, _aggregate_layer_health,
    SCHEMA_VERSION, HAS_EXCEL
)

SERIES_DIR = Path(r"O:\_Theophysics_v4\04_THEOPYHISCS\___THE CONVERGENCE TX 6.6")
OUTPUT_DIR = Path(r"T:\THEOPHYSICS_PAPER_INTELLIGENCE\OUTPUT\CONVERGENCE_TX_6.6")

# Files to skip (meta, indexes, non-content)
SKIP_PATTERNS = [
    r'^00_',                    # front door / index
    r'^_',                      # _CLAUDIAN_AUDIT, _CONVERGENCE_MASTER_INDEX, __MASTER
    r'excalidraw',              # drawing files
    r'PIPELINE_POINTER',        # pipeline pointer
    r'WEB_TEMPLATE_TYPE',       # template reference
    r'DUPLICATE',               # known duplicates
]


def should_skip(name: str) -> bool:
    for pat in SKIP_PATTERNS:
        if re.search(pat, name, re.IGNORECASE):
            return True
    return False


def write_vault_markdown(row: dict, out_dir: Path):
    """Write a vault-ready markdown scorecard for one paper."""
    fname = row.get('file', 'unknown')
    slug = fname.replace('.md', '')

    lines = []
    lines.append("---")
    lines.append(f"paper_id: {row.get('paper_id', '')}")
    lines.append(f"source: {fname}")
    lines.append(f"schema_version: {row.get('schema_version', '')}")
    lines.append(f"analyzed_at: {row.get('analyzed_at', '')}")
    lines.append(f"series: Convergence TX 6.6")
    lines.append("type: paper-intelligence")
    lines.append("---")
    lines.append("")
    lines.append(f"# Paper Intelligence: {slug.replace('_', ' ')}")
    lines.append("")

    # L1 Text Analytics
    lines.append("## L1 — Text Analytics")
    lines.append(f"- **Word count**: {row.get('L1_word_count', 'N/A')}")
    lines.append(f"- **Reading level**: {row.get('L1_text_standard', 'N/A')}")
    lines.append(f"- **Flesch-Kincaid grade**: {row.get('L1_flesch_kincaid_grade', 'N/A')}")
    lines.append(f"- **Flesch reading ease**: {row.get('L1_flesch_reading_ease', 'N/A')}")
    lines.append(f"- **Vocab richness**: {row.get('L1_vocab_richness', 'N/A')}")
    lines.append(f"- **Reading time**: {row.get('L1_reading_time_min', 'N/A')} min")
    kw = row.get('L1_keybert_keywords', '')
    if kw:
        lines.append(f"- **Keywords**: {kw[:200]}")
    lines.append("")

    # L2 Academic Standard
    lines.append("## L2 — Academic Standard")
    lines.append(f"- **Grade**: {row.get('L2_academic_grade', 'N/A')}")
    lines.append(f"- **Citations**: {row.get('L2_citation_count', 0)}")
    lines.append(f"- **External theories**: {row.get('L2_external_theory_count', 0)}")
    lines.append(f"- **Structure**: {row.get('L2_structure_score', 'N/A')}")
    theories = row.get('L2_external_theories', '')
    if theories:
        lines.append(f"- **Theories referenced**: {theories}")
    lines.append("")

    # L3 Theophysics Metrics
    lines.append("## L3 — Theophysics Metrics")
    lines.append(f"- **CHI score**: {row.get('L3_chi_score', 'N/A')} ({row.get('L3_chi_status', '')})")
    lines.append(f"- **W/K ratio**: {row.get('L3_wk_ratio', 'N/A')} ({row.get('L3_wk_status', '')})")
    lines.append(f"- **Fruits composite**: {row.get('L3_fruits_composite', 'N/A')}")
    lines.append(f"- **Dominant fruit**: {row.get('L3_dominant_fruit', 'N/A')}")
    lines.append(f"- **CKG tier**: {row.get('L3_ckg_tier', 'N/A')}")
    lines.append(f"- **Scripture refs**: {row.get('L3_scripture_refs', 0)}")
    lines.append(f"- **Master Equation avg**: {row.get('L3_me_avg_score', 'N/A')}")
    lines.append(f"- **ME dominant variable**: {row.get('L3_me_dominant_variable', 'N/A')}")
    lines.append("")

    # L5 NLP Deep
    lines.append("## L5 — NLP Deep")
    lines.append(f"- **Entity count**: {row.get('L5_entity_count', 'N/A')}")
    lines.append(f"- **Topic count**: {row.get('L5_topic_count', 'N/A')}")
    people = row.get('L5_entity_people', '')
    if people:
        lines.append(f"- **People**: {people}")
    orgs = row.get('L5_entity_orgs', '')
    if orgs:
        lines.append(f"- **Orgs/Frameworks**: {orgs}")
    lines.append("")

    # L6 Truth Engine
    lines.append("## L6 — Truth Engine")
    lines.append(f"- **Truth score**: {row.get('L6_truth_score', 'N/A')}")
    lines.append(f"- **Coherence score**: {row.get('L6_coherence_score', 'N/A')}")
    lines.append(f"- **Combined score**: {row.get('L6_combined_score', 'N/A')}")
    lines.append(f"- **Evidence density**: {row.get('L6_evidence_density', 'N/A')}")
    lines.append(f"- **Contradiction flags**: {row.get('L6_contradiction_flags', 0)}")
    lines.append(f"- **Claims analyzed**: {row.get('L6_claim_count', 0)}")
    lines.append(f"  - Anchored: {row.get('L6_anchored_claims', 0)}")
    lines.append(f"  - Under-supported: {row.get('L6_under_supported_claims', 0)}")
    lines.append(f"  - Overstated: {row.get('L6_overstated_claims', 0)}")
    lines.append(f"  - Falsifiable: {row.get('L6_falsifiable_claims', 0)}")
    lines.append("")

    # Fruits breakdown
    lines.append("### Fruits of the Spirit")
    for fruit in ['love', 'joy', 'peace', 'patience', 'kindness', 'goodness',
                  'faithfulness', 'gentleness', 'self_control']:
        val = row.get(f'L6_fruit_{fruit}', 0)
        anti = row.get(f'L6_anti_{fruit}', 0)
        bar = '█' * int((val or 0) * 30)
        lines.append(f"- **{fruit.replace('_', ' ').title()}**: {val:.3f} (anti: {anti:.3f}) {bar}")
    lines.append(f"- **Fruit integrity**: {row.get('L6_fruit_integrity_score', 'N/A')}")
    lines.append(f"- **Anti-fruit pressure**: {row.get('L6_anti_fruit_pressure', 'N/A')}")
    lines.append("")

    # Character profile
    lines.append("### Character Profile")
    lines.append(f"- **Posture**: {row.get('L6_character_posture', 'N/A')}")
    lines.append(f"- **Integrity profiles**: {row.get('L6_integrity_profiles', 'N/A')}")
    lines.append(f"- **Threat score**: {row.get('L6_threat_score', 0)}")
    lines.append(f"- **Protection score**: {row.get('L6_protection_score', 0)}")
    threats = row.get('L6_primary_threats', '')
    protections = row.get('L6_primary_protections', '')
    if threats:
        lines.append(f"- **Primary threats**: {threats}")
    if protections:
        lines.append(f"- **Primary protections**: {protections}")
    lines.append("")

    # L7 Graph (if available)
    centrality = row.get('L7_centrality_within_series', '')
    cluster = row.get('L7_cluster', '')
    if centrality or cluster:
        lines.append("## L7 — Knowledge Graph")
        lines.append(f"- **Centrality**: {centrality}")
        lines.append(f"- **Cluster**: {cluster}")
        lines.append("")

    # L8 Emotion Profile
    lines.append("## L8 — Emotion Profile")
    lines.append("")
    lines.append("### NRC Plutchik (lexicon-based)")
    lines.append(f"- **Top emotions**: {row.get('L8_nrc_top_emotions', 'N/A')}")
    lines.append(f"- Trust: {row.get('L8_nrc_trust', 0)} | Joy: {row.get('L8_nrc_joy', 0)} | Anticipation: {row.get('L8_nrc_anticipation', 0)}")
    lines.append(f"- Fear: {row.get('L8_nrc_fear', 0)} | Anger: {row.get('L8_nrc_anger', 0)} | Sadness: {row.get('L8_nrc_sadness', 0)}")
    lines.append(f"- Positive: {row.get('L8_nrc_positive', 0)} | Negative: {row.get('L8_nrc_negative', 0)}")
    lines.append("")
    lines.append("### GoEmotions (27 fine-grained, BERT-based)")
    lines.append(f"- **Dominant**: {row.get('L8_emo_dominant', 'N/A')}")
    lines.append(f"- **Top 5**: {row.get('L8_emo_top_5', 'N/A')}")
    lines.append("")
    lines.append("### Emotion → Fruits of the Spirit Mapping")
    for fruit in ['love', 'joy', 'peace', 'patience', 'kindness', 'goodness',
                  'faithfulness', 'gentleness', 'self_control']:
        val = row.get(f'L8_fruit_emo_{fruit}', 0) or 0
        bar = '█' * int(val * 20)
        lines.append(f"- **{fruit.replace('_', ' ').title()}**: {val:.3f} {bar}")
    lines.append("")
    lines.append("### Anti-Fruit Emotional Signals")
    for anti in ['hatred', 'despair', 'conflict', 'impatience', 'cruelty',
                 'corruption', 'betrayal', 'harshness', 'indulgence']:
        val = row.get(f'L8_anti_emo_{anti}', 0) or 0
        bar = '▓' * int(val * 100) if val > 0.01 else ''
        lines.append(f"- **{anti.title()}**: {val:.4f} {bar}")
    lines.append("")
    lines.append(f"- **Fruit composite**: {row.get('L8_fruit_emo_composite', 'N/A')}")
    lines.append(f"- **Anti-fruit composite**: {row.get('L8_anti_emo_composite', 'N/A')}")
    lines.append(f"- **Net fruit score**: {row.get('L8_fruit_emo_net', 'N/A')}")
    lines.append("")

    # L9 Linguistic Depth
    lines.append("## L9 — Linguistic Depth")
    lines.append("### Vocabulary Diversity")
    lines.append(f"- **MTLD**: {row.get('L9_lr_mtld', 'N/A')} (Measure of Textual Lexical Diversity)")
    lines.append(f"- **MATTR**: {row.get('L9_lr_mattr', 'N/A')} (Moving Average TTR)")
    lines.append(f"- **HD-D**: {row.get('L9_lr_hdd', 'N/A')} (vocd-D)")
    lines.append(f"- **TTR**: {row.get('L9_lr_ttr', 'N/A')} | **Root TTR**: {row.get('L9_lr_rttr', 'N/A')}")
    lines.append(f"- **Unique terms**: {row.get('L9_lr_terms', 'N/A')} / {row.get('L9_lr_words', 'N/A')} words")
    lines.append("")

    # L10 Idea Density
    lines.append("## L10 — Idea Density")
    lines.append(f"- **Mean density**: {row.get('L10_idea_density_mean', 'N/A')}")
    lines.append(f"- **Range**: {row.get('L10_idea_density_min', 'N/A')} – {row.get('L10_idea_density_max', 'N/A')}")
    lines.append(f"- **Std dev**: {row.get('L10_idea_density_std', 'N/A')}")
    lines.append(f"- **Total propositions**: {row.get('L10_idea_total_propositions', 'N/A')}")
    lines.append(f"- **Level**: {row.get('L10_idea_density_level', 'N/A')}")
    lines.append("")

    # Layer health
    status = row.get('_layer_status', {})
    lines.append("## Layer Health")
    for layer, st in sorted(status.items()):
        icon = '✅' if st == 'ok' else ('⏭️' if st == 'skipped' else '❌')
        lines.append(f"- {layer}: {icon} {st}")
    lines.append("")

    md_path = out_dir / f"PI_{slug}.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Gather papers
    all_md = sorted(SERIES_DIR.glob("*.md"))
    papers = [f for f in all_md if not should_skip(f.name)]

    print(f"Convergence TX 6.6 — Full Pipeline Run")
    print(f"Papers found: {len(papers)} (skipped {len(all_md) - len(papers)} meta files)")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Schema: {SCHEMA_VERSION}")
    print(f"{'='*60}")

    series_id = f"S-convergence-tx66"
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    all_rows = []
    vault_dir = OUTPUT_DIR / "vault_scorecards"
    vault_dir.mkdir(parents=True, exist_ok=True)

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] {paper.name}")
        row = analyze_paper(
            str(paper),
            run_openai=False,
            series_id=series_id,
            run_id=run_id
        )
        all_rows.append(row)

        # Write vault-ready markdown
        md_path = write_vault_markdown(row, vault_dir)
        print(f"  Vault MD: {md_path.name}")

    # L7 Knowledge Graph (needs all rows)
    print(f"\n{'='*60}")
    print("Building L7 Knowledge Graph...")
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "07_KNOWLEDGE_GRAPHS"))
        import graph_builder as L7
        graph_result = L7.build_graph(all_rows, str(OUTPUT_DIR))
        for row in all_rows:
            g = graph_result.get('node_data', {}).get(row['file'], {})
            row['L7_centrality_within_series'] = g.get('centrality', '')
            row['L7_cluster'] = g.get('cluster', '')
            row['_layer_status']['L7'] = "ok"
        print("  [OK] L7 Knowledge Graph")
    except Exception as e:
        print(f"  [ERROR] L7 Knowledge Graph: {e}")
        for row in all_rows:
            row['_layer_status']['L7'] = "error"

    # Excel output
    if HAS_EXCEL and all_rows:
        excel_path = OUTPUT_DIR / f"CONVERGENCE_TX66_PAPER_INTELLIGENCE_{run_id}.xlsx"
        write_excel(all_rows, excel_path)
        print(f"\n  Excel: {excel_path}")

    # JSON backup
    json_path = OUTPUT_DIR / f"CONVERGENCE_TX66_pipeline_results_{run_id}.json"
    clean_rows = [{k: v for k, v in r.items() if not k.startswith('_')} for r in all_rows]
    json_path.write_text(json.dumps(clean_rows, indent=2, default=str), encoding='utf-8')
    print(f"  JSON:  {json_path}")

    # Run summary
    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "series_id": series_id,
        "series_name": "Convergence TX 6.6",
        "paper_count": len(all_rows),
        "output_dir": str(OUTPUT_DIR),
        "layer_health": _aggregate_layer_health(all_rows),
        "papers": [{"paper_id": r.get("paper_id"), "file": r.get("file"),
                     "status": r.get("_layer_status", {})} for r in all_rows],
    }
    summary_path = OUTPUT_DIR / f"run_summary_{run_id}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"COMPLETE — {len(all_rows)} papers analyzed")
    print(f"Layer health: {summary['layer_health']}")
    print(f"Vault scorecards: {vault_dir}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
