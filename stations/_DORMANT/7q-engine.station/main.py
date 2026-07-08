"""
7Q Engine v2 — Main CLI Entry Point.

Modes:
  forward   — Interactive intake Q0→Q7 → score → Obsidian note
  backward  — Destruction mode Q7→Q1 → score → Obsidian note
  llm-full  — Send claim to OpenAI for LLM Maximum Rigor analysis
  llm-judge — Send a prior assessment to the LLM judge
  score     — Quick score from command line args
  test      — Run the built-in test claim

David Lowe | POF 2828 | March 2026
"""

import sys
import os

# Add engine directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from intake import run_forward_intake, banner
from destroy import run_backward_destruction
from obsidian_writer import write_note, build_full_note
from html_report import write_html_report
from scorer import (
    ClaimProfile, EvidenceItem, PredictionItem, DeathTest,
    compute_truth_score, score_summary, machine_block,
)
from llm_bridge import (
    run_full_analysis, run_compact_analysis, run_judge,
    parse_scoring_block, parse_knowledge_graph,
)


def print_usage():
    print("""
╔═══════════════════════════════════════════════╗
║          7Q ENGINE v2 — CLI                   ║
║   David Lowe | POF 2828 | March 2026          ║
╚═══════════════════════════════════════════════╝

Usage:
  python main.py forward       Interactive forward intake (Q0→Q7)
  python main.py backward      Destruction mode (Q7→Q1)
  python main.py llm-full      LLM Maximum Rigor analysis
  python main.py llm-compact   LLM compact scoring
  python main.py llm-judge     Judge a prior assessment
  python main.py test          Run test claim through scorer
  python main.py               Show this help

Options:
  --no-write    Don't write Obsidian note (just print score)
  --output DIR  Custom output directory for .md files
  --model NAME  LLM model to use (default: gpt-4o)
""")


def mode_forward(write_obsidian: bool = True, output_dir: str = None):
    """Run forward intake mode."""
    profile, result = run_forward_intake()

    if write_obsidian:
        filepath = write_note(profile, result, mode="forward", output_dir=output_dir)
        print(f"\n  Obsidian note: {filepath}")
        html_path = write_html_report(profile, result, mode="forward", output_dir=output_dir)
        print(f"  HTML report:   {html_path}")

    return profile, result


def mode_backward(write_obsidian: bool = True, output_dir: str = None):
    """Run backward destruction mode."""
    profile, result = run_backward_destruction()

    if write_obsidian:
        filepath = write_note(profile, result, mode="backward", output_dir=output_dir)
        print(f"\n  Obsidian note: {filepath}")
        html_path = write_html_report(profile, result, mode="backward", output_dir=output_dir)
        print(f"  HTML report:   {html_path}")

    return profile, result


def mode_llm_full(model: str = "gpt-4o", write_obsidian: bool = True, output_dir: str = None):
    """Run LLM full analysis mode."""
    banner("7Q LLM MAXIMUM RIGOR")

    claim_text = input("  Claim text: ").strip()
    claim_id = input("  Claim ID [CL-UNV-0001]: ").strip() or "CL-UNV-0001"
    domain = input("  Domain [UNV]: ").strip().upper() or "UNV"

    response = run_full_analysis(claim_text, claim_id, domain, model=model)
    if response:
        print("\n" + "═" * 55)
        print("  LLM ANALYSIS RESULT")
        print("═" * 55)
        print(response)

        # Parse and display scoring block
        scores = parse_scoring_block(response)
        if scores:
            print("\n  Parsed scores:")
            for k, v in scores.items():
                print(f"    {k}: {v}")

        # Save raw response
        if write_obsidian:
            d = output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "scored_output")
            os.makedirs(d, exist_ok=True)
            filepath = os.path.join(d, f"{claim_id}_llm_full.md")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"---\ntype: 7Q-llm-analysis\nid: {claim_id}\ndomain: {domain}\nmodel: {model}\n---\n\n")
                f.write(f"# 7Q LLM Analysis: {claim_text}\n\n")
                f.write(response)
            print(f"\n  Saved to: {filepath}")
    else:
        print("  Analysis failed. Check API key and connection.")


def mode_llm_judge(model: str = "gpt-4o"):
    """Run LLM judge on a prior assessment."""
    banner("7Q LLM JUDGE")

    print("  Paste the prior assessment (end with a line containing only 'END'):")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    assessment = "\n".join(lines)
    response = run_judge(assessment, model=model)
    if response:
        print("\n" + "═" * 55)
        print("  JUDGE VERDICT")
        print("═" * 55)
        print(response)
    else:
        print("  Judge failed. Check API key and connection.")


def mode_test():
    """Run the built-in test claim through the full pipeline."""
    banner("7Q TEST — Planet Orbital Mechanics")

    profile = ClaimProfile(
        claim_id="CL-PHY-0001",
        claim_text="Planet size and position follow predictable patterns based on orbital mechanics",
        domain="PHY",
        mode="INVEST",
        entity_type="LAW",
        axiom_class="DERIVED",
        status="CANONICAL",
        source="PEERREV",
        scales=["COSMIC"],
        iso_status="CONFIRMED",
        cross_domain_key="ISO2",
        domains_present=["PHY", "MTH"],
        claim_type="MATHEMATICAL",
        precision="PRECISE",
        certainty="PROVEN",
        scope="UNIVERSAL",
        evidence=[
            EvidenceItem(
                name="Kepler's laws + centuries of observation",
                evidence_type="EXPERIMENTAL",
                tier="T1",
                strength="CONCLUSIVE",
                linkage="DIRECT",
                ps_raw=0.95,
                ed=0.90,
                ec=0.85,
            ),
            EvidenceItem(
                name="Exoplanet surveys (Kepler/TESS)",
                evidence_type="OBSERVATIONAL",
                tier="T1",
                strength="STRONG",
                linkage="DIRECT",
                ps_raw=0.85,
                ed=0.80,
                ec=0.75,
            ),
        ],
        terminus="EMPIRICAL",
        derivation="DEDUCTIVE",
        predictions=[
            PredictionItem(
                description="Next planet position from orbital elements",
                pred_type="CONFIRMED",
                competing="EXCLUSIVE",
                confirmed=True,
            ),
        ],
        death_tests=[
            DeathTest(death_type="SELFREF", result="SURVIVES"),
            DeathTest(death_type="REGRESS", result="SURVIVES"),
            DeathTest(death_type="EMPIRICAL", result="SURVIVES", notes="Centuries of observation"),
            DeathTest(death_type="INCOHERENT", result="SURVIVES"),
            DeathTest(death_type="EXPLAIN", result="SURVIVES", notes="No competing model works better"),
        ],
        robustness="SURVIVED_ADV",
        cascade_scope="FRAMEWORK",
    )

    result = compute_truth_score(profile)
    print(score_summary(result))
    print()
    print(machine_block(profile, result))

    # Write test note + HTML report
    filepath = write_note(profile, result, mode="test")
    print(f"\n  Test note written to: {filepath}")
    html_path = write_html_report(profile, result, mode="test")
    print(f"  HTML report:         {html_path}")

    return profile, result


# ═══════════════════════════════════════════════
# CLI PARSER
# ═══════════════════════════════════════════════

def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    mode = args[0].lower()
    write_obsidian = "--no-write" not in args
    output_dir = None
    model = "gpt-4o"

    for i, arg in enumerate(args):
        if arg == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
        if arg == "--model" and i + 1 < len(args):
            model = args[i + 1]

    if mode == "forward":
        mode_forward(write_obsidian, output_dir)
    elif mode == "backward":
        mode_backward(write_obsidian, output_dir)
    elif mode == "llm-full":
        mode_llm_full(model, write_obsidian, output_dir)
    elif mode == "llm-compact":
        banner("7Q LLM COMPACT SCORING")
        claim = input("  Claim text: ").strip()
        cid = input("  Claim ID [CL-UNV-0001]: ").strip() or "CL-UNV-0001"
        dom = input("  Domain [UNV]: ").strip().upper() or "UNV"
        resp = run_compact_analysis(claim, cid, dom, model=model)
        if resp:
            print(resp)
    elif mode == "llm-judge":
        mode_llm_judge(model)
    elif mode == "test":
        mode_test()
    else:
        print(f"  Unknown mode: {mode}")
        print_usage()


if __name__ == "__main__":
    main()
