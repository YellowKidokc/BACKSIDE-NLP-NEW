"""
pipeline.py — χ-Evaluator v2 Station Pipeline
Reads claims from _inbox, evaluates, writes results to _outbox.

Usage:
  python pipeline.py                    # process all files in _inbox
  python pipeline.py --claim "text"     # evaluate a single claim
  python pipeline.py --demo             # run built-in demo
"""
import sys, os, json, glob
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from chi_engine import (
    ChannelResult, PressureResult, FruitOutput,
    ChiEvaluation, tanh_fruit_score, product, CHANNELS
)
from prompt import build_prompt

STATION_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(STATION_DIR, "_inbox")
OUTBOX = os.path.join(STATION_DIR, "_outbox")


def demo_evaluate():
    """Built-in demo with manual scores."""
    claim = "Truth does not require falsehood, but falsehood requires truth."
    channels = [
        ChannelResult.build("G",     0.80, 0.05, +1, 0.80, "Acknowledges dependency asymmetry."),
        ChannelResult.build("M",     0.90, 0.05, +1, 0.85, "Aligns with logical priority structure."),
        ChannelResult.build("E",     0.95, 0.02, +1, 0.90, "Clear and compressible signal."),
        ChannelResult.build("S_eff", 0.90, 0.03, +1, 0.85, "Reduces disorder."),
        ChannelResult.build("T",     0.88, 0.04, +1, 0.80, "Not urgency-dependent."),
        ChannelResult.build("K",     0.96, 0.02, +1, 0.90, "Compresses to one sentence."),
        ChannelResult.build("R",     0.70, 0.10,  0, 0.70, "Reframes but does not force."),
        ChannelResult.build("Q",     0.95, 0.01, +1, 0.90, "Invites inspection; no coercion."),
        ChannelResult.build("F",     0.85, 0.05, +1, 0.80, "Applies across logic, morality, theology."),
        ChannelResult.build("C",     0.92, 0.03, +1, 0.85, "Integrates with larger framework."),
    ]
    pressure = [
        PressureResult("static", 0.45, "Strong initial coherence."),
        PressureResult("compression", 0.55, "Improves when compressed."),
        PressureResult("strongest_objection", 0.49, "Survives with minor clarification."),
        PressureResult("time", 0.58, "Not urgency-dependent."),
        PressureResult("fruit", 0.61, "Tends toward clarity and peace."),
    ]
    ev = ChiEvaluation(
        claim=claim, claim_type="analytic", compressed_claim=claim,
        channel_results=channels, pressure_results=pressure,
        fruit_output=FruitOutput(
            dominant_fruits=["Peace","Goodness","Self-Control"],
            fruit_score=tanh_fruit_score(product([c.effective_score for c in channels])),
            notes="Clarifies rather than manipulates."
        ),
        final_report="Structurally coherent. Improves under compression."
    ).compute()
    return ev


def save_result(ev, source_name="manual"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"CHI_{ts}__ST_CHI__{source_name}.json"
    path = os.path.join(OUTBOX, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ev.to_json())
    print(f"[chi-evaluator] Saved: {path}")
    compact = ev.to_compact()
    print(f"[chi-evaluator] chi={compact['chi']:.6f} | verdict={compact['verdict']} | gradient={compact['gradient']}")
    return path


if __name__ == "__main__":
    if "--demo" in sys.argv:
        ev = demo_evaluate()
        save_result(ev, "demo")
        print(ev.to_json())

    elif "--claim" in sys.argv:
        idx = sys.argv.index("--claim")
        claim_text = " ".join(sys.argv[idx+1:])
        print(f"[chi-evaluator] Claim: {claim_text[:80]}...")
        print("[chi-evaluator] LLM prompt generated. Send to API for scoring.")
        prompt = build_prompt(claim_text)
        print(json.dumps(prompt, indent=2))

    else:
        # Process inbox
        files = glob.glob(os.path.join(INBOX, "*.md")) + glob.glob(os.path.join(INBOX, "*.txt"))
        if not files:
            print("[chi-evaluator] No files in _inbox. Use --demo or --claim.")
        for f in files:
            print(f"[chi-evaluator] Would process: {f}")
            print("[chi-evaluator] Full pipeline requires LLM API integration.")
