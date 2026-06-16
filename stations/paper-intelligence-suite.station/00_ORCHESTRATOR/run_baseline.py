"""
BASELINE COMPARISON RUN
========================
Runs the pipeline on samples from 4 contrasting corpora + Convergence TX 6.6
to establish baseline metrics and test discrimination power.

Corpora:
  1. Convergence TX 6.6 (Theophysics originals) — should score highest on theo metrics
  2. Evolution probe papers — scientific/naturalist, should differ on CHI/fruits
  3. Consciousness theories — academic, different ME variable profile
  4. Worldviews — philosophical, diverse fruit/emotion profiles
  5. Presidential inaugurals — political rhetoric, very different posture
"""
import sys, json, re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_pipeline import (
    analyze_paper, write_excel, _aggregate_layer_health,
    SCHEMA_VERSION, HAS_EXCEL
)

OUTPUT_DIR = Path(r"T:\THEOPHYSICS_PAPER_INTELLIGENCE\OUTPUT\BASELINE_COMPARISON")

CORPORA = {
    'CONVERGENCE': {
        'path': Path(r"O:\_Theophysics_v4\04_THEOPYHISCS\___THE CONVERGENCE TX 6.6"),
        'samples': ['HOLDING_GOD_ACCOUNTABLE.md', 'Genesis_as_Quantum_Event.md',
                     'SALVATION_IS_A_PHASE_TRANSITION.md', 'THE_DAY_TIME_BEGAN.md',
                     'MATH_IS_MORAL.md'],
    },
    'EVOLUTION': {
        'path': Path(r"O:\_Theophysics_v4\00_Canonical\Evolution"),
        'samples': ['SP01_Haldane_Rate_Problem.md', 'SP02_Barrick_LTEE_Mismatch.md',
                     'SP03_Computational_Model_Circularity.md', 'SP05_Cambrian_Lynch_Abegg.md',
                     'SP06_Blount_Citrate.md'],
    },
    'CONSCIOUSNESS': {
        'path': Path(r"O:\_Theophysics_v4\00_Canonical\TH_Consciousness"),
        'samples': ['Global_Consciousness_Project_CLEAN.md', 'Global_Workspace_Theory_CLEAN.md',
                     'Integrated_Information_Theory_(Tononi)_CLEAN.md',
                     'Orch_OR_(Penrose-Hameroff)_CLEAN.md',
                     'Participatory_Anthropic_Principle_(PAP)_CLEAN.md'],
    },
    'WORLDVIEWS': {
        'path': Path(r"O:\_Theophysics_v4\00_Canonical\Worldviews"),
        'samples': ['Absurdism.md', 'Aristotelianism.md', 'Calvinism.md',
                     'Confucianism.md'],
    },
    'INAUGURAL': {
        'path': Path(r"O:\_Theophysics_v4\00_Canonical\inaugural"),
        'samples': ['1789-Washington.md', '1801-Jefferson.md',
                     '1861-Lincoln.md', '1933-Roosevelt.md', '1961-Kennedy.md'],
    },
}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')

    all_rows = []
    for corpus_name, config in CORPORA.items():
        base = config['path']
        samples = config['samples']

        print(f"\n{'='*60}")
        print(f"CORPUS: {corpus_name}")
        print(f"{'='*60}")

        for fname in samples:
            paper = base / fname
            if not paper.exists():
                print(f"  SKIP (not found): {fname}")
                continue

            print(f"\n  [{corpus_name}] {fname}")
            row = analyze_paper(str(paper), run_openai=False,
                                series_id=f"baseline-{corpus_name.lower()}",
                                run_id=run_id)
            row['_corpus'] = corpus_name
            all_rows.append(row)

    # Write Excel
    if HAS_EXCEL and all_rows:
        excel_path = OUTPUT_DIR / f"BASELINE_COMPARISON_{run_id}.xlsx"
        write_excel(all_rows, excel_path)
        print(f"\n  Excel: {excel_path}")

    # Write JSON
    json_rows = [{k: v for k, v in r.items() if not k.startswith('_')}
                 for r in all_rows]
    # Add corpus tag back
    for i, r in enumerate(all_rows):
        json_rows[i]['corpus'] = r.get('_corpus', '')

    json_path = OUTPUT_DIR / f"baseline_results_{run_id}.json"
    json_path.write_text(json.dumps(json_rows, indent=2, default=str), encoding='utf-8')

    # ── COMPARISON SUMMARY ──
    print(f"\n\n{'='*60}")
    print(f"BASELINE COMPARISON SUMMARY")
    print(f"{'='*60}")

    # Group by corpus
    from collections import defaultdict
    groups = defaultdict(list)
    for r in all_rows:
        groups[r['_corpus']].append(r)

    # Key metrics to compare
    metrics = [
        ('L3_chi_score', 'CHI'),
        ('L6_truth_score', 'Truth'),
        ('L6_coherence_score', 'Coherence'),
        ('L6_combined_score', 'Combined'),
        ('L6_evidence_density', 'Evidence'),
        ('L6_contradiction_flags', 'Contradictions'),
        ('L3_fruits_composite', 'Fruits(L3)'),
        ('L8_fruit_emo_composite', 'Fruits(L8)'),
        ('L8_anti_emo_composite', 'Anti-Fruits'),
        ('L8_fruit_emo_net', 'Fruit Net'),
        ('L10_idea_density_mean', 'Idea Density'),
        ('L9_lr_mtld', 'MTLD'),
        ('L8_nrc_trust', 'NRC Trust'),
        ('L8_nrc_positive', 'NRC Positive'),
        ('L8_nrc_negative', 'NRC Negative'),
        ('L3_scripture_refs', 'Scripture'),
    ]

    # Print header
    header = f"{'Corpus':<16}"
    for _, label in metrics:
        header += f"{label:>12}"
    print(header)
    print("-" * len(header))

    for corpus_name in CORPORA:
        rows = groups.get(corpus_name, [])
        if not rows:
            continue
        line = f"{corpus_name:<16}"
        for key, _ in metrics:
            vals = [r.get(key, 0) or 0 for r in rows if isinstance(r.get(key, 0), (int, float))]
            if vals:
                avg = sum(vals) / len(vals)
                line += f"{avg:>12.3f}"
            else:
                line += f"{'N/A':>12}"
        print(line)

    print(f"\n{len(all_rows)} papers analyzed across {len(groups)} corpora")
    print(f"Results: {OUTPUT_DIR}")

    # Generate HTML reports too
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "11_HTML_REPORT"))
        from generate_report import generate_paper_html
        html_dir = OUTPUT_DIR / "html_reports"
        html_dir.mkdir(exist_ok=True)
        for r in all_rows:
            corpus = r.get('_corpus', 'unknown')
            fname = r.get('file', 'unknown').replace('.md', '')
            html = generate_paper_html(r)
            path = html_dir / f"BL_{corpus}_{fname}.html"
            path.write_text(html, encoding='utf-8')
        print(f"HTML reports: {html_dir}")
    except Exception as e:
        print(f"HTML generation error: {e}")


if __name__ == '__main__':
    main()
