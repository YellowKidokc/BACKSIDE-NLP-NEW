"""
chi_engine.py — χ-Evaluator v2 Core Engine
Theophysics Master Equation coherence diagnostic
POF 2828 | June 2026

χ = G · M · E · S_eff · T · K · R · Q · F · C
Product, not sum. Zero channel = total collapse.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Literal
import json, math, statistics

ChannelCode = Literal["G","M","E","S_eff","T","K","R","Q","F","C"]
Verdict = Literal["coherent","partially coherent","fragile","high-signal deception","collapsed","repairable"]
GradientLabel = Literal["positive","neutral","negative","unstable"]

CHANNELS: dict[str, str] = {
    "G":     "External input / dependency honesty",
    "M":     "Alignment / reference standard",
    "E":     "Truth / signal fidelity",
    "S_eff": "Entropy / disorder cost",
    "T":     "Temporal persistence",
    "K":     "Compression / wisdom density",
    "R":     "Phase transition / justified regime change",
    "Q":     "Free will / invitation vs coercion",
    "F":     "Cross-context binding",
    "C":     "Integration / whole-system coherence",
}

PRESSURE_STATES = [
    "static", "compression", "strongest_objection", "time",
    "translation", "evidence", "implementation", "fruit",
    "falsification", "hostile_misuse",
]

FRUITS = ["Love","Joy","Peace","Patience","Kindness","Goodness","Faithfulness","Gentleness","Self-Control"]
ANTIFRUITS = ["Hatred","Despair","Anxiety","Impatience","Cruelty","Corruption","Betrayal","Harshness","Addiction"]


def clamp01(x: float) -> float:
    if x is None or math.isnan(x):
        return 0.0
    return max(0.0, min(1.0, float(x)))


def product(values: list[float]) -> float:
    result = 1.0
    for v in values:
        result *= clamp01(v)
    return result


def tanh_fruit_score(chi: float, beta: float = 4.0, chi_c: float = 0.30) -> float:
    raw = math.tanh(beta * (chi - chi_c))
    return round((raw + 1.0) / 2.0, 6)


def simple_slope(xs: list[float], ys: list[float]) -> float:
    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)
    denom = sum((x - mean_x) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denom


@dataclass
class ChannelResult:
    channel: str
    name: str
    v_pos: float
    v_neg: float
    effective_score: float
    gradient_direction: int
    confidence: float
    reasoning: str
    evidence: str = ""
    failure_mode: str = ""
    repair_path: str = ""

    @classmethod
    def build(cls, channel, v_pos, v_neg, gradient_direction, confidence, reasoning,
              evidence="", failure_mode="", repair_path=""):
        vp = clamp01(v_pos)
        vn = clamp01(v_neg)
        return cls(
            channel=channel, name=CHANNELS.get(channel, channel),
            v_pos=vp, v_neg=vn,
            effective_score=round(vp * (1.0 - vn), 6),
            gradient_direction=max(-1, min(1, int(gradient_direction))),
            confidence=clamp01(confidence),
            reasoning=reasoning, evidence=evidence,
            failure_mode=failure_mode, repair_path=repair_path,
        )


@dataclass
class PressureResult:
    pressure_state: str
    chi: float
    notes: str = ""


@dataclass
class FruitOutput:
    dominant_fruits: list[str] = field(default_factory=list)
    dominant_antifruits: list[str] = field(default_factory=list)
    fruit_score: float = 0.5
    notes: str = ""


def infer_gradient(channels, pressure_results):
    if pressure_results and len(pressure_results) >= 3:
        chis = [max(1e-9, clamp01(p.chi)) for p in pressure_results]
        logs = [math.log(x) for x in chis]
        slope = simple_slope(list(range(len(logs))), logs)
        if slope > 0.05: return "positive"
        if slope < -0.05: return "negative"
        return "neutral"
    directions = [c.gradient_direction for c in channels]
    total = sum(directions)
    if any(c.effective_score < 0.05 and c.gradient_direction < 0 for c in channels):
        return "unstable"
    if total >= 3: return "positive"
    if total <= -3: return "negative"
    return "neutral"


def infer_verdict(chi, zero_channels, gradient, channels):
    if zero_channels:
        fatal = {"coercion","contradiction","self-sealing","unfalsifiable","circular validation"}
        modes = {c.failure_mode.lower().strip() for c in channels if c.channel in zero_channels}
        if modes & fatal: return "collapsed"
        return "repairable"
    cmap = {c.channel: c for c in channels}
    if (cmap["E"].effective_score > 0.70 and (
            cmap["Q"].effective_score < 0.25 or
            cmap["K"].effective_score < 0.25 or
            cmap["T"].effective_score < 0.25)):
        return "high-signal deception"
    if chi > 0.50 and gradient in {"positive","neutral"}: return "coherent"
    if 0.10 <= chi <= 0.50: return "partially coherent"
    if 0.01 <= chi < 0.10: return "fragile"
    return "collapsed" if gradient == "negative" else "repairable"


@dataclass
class ChiEvaluation:
    claim: str
    claim_type: str
    compressed_claim: str
    channel_results: list[ChannelResult]
    pressure_results: list[PressureResult] = field(default_factory=list)
    fruit_output: FruitOutput = field(default_factory=FruitOutput)
    final_report: str = ""
    static_chi: float = 0.0
    gradient: GradientLabel = "neutral"
    zero_channels: list[str] = field(default_factory=list)
    weakest_channels: list[str] = field(default_factory=list)
    strongest_channels: list[str] = field(default_factory=list)
    verdict: Verdict = "fragile"

    def compute(self):
        scores = [c.effective_score for c in self.channel_results]
        self.static_chi = round(product(scores), 8)
        self.zero_channels = [c.channel for c in self.channel_results if c.effective_score <= 1e-6]
        sc = sorted(self.channel_results, key=lambda c: c.effective_score)
        self.weakest_channels = [c.channel for c in sc[:3]]
        self.strongest_channels = [c.channel for c in sc[-3:]][::-1]
        self.gradient = infer_gradient(self.channel_results, self.pressure_results)
        self.verdict = infer_verdict(self.static_chi, self.zero_channels, self.gradient, self.channel_results)
        if not self.fruit_output.fruit_score:
            self.fruit_output.fruit_score = tanh_fruit_score(self.static_chi)
        return self

    def to_json(self):
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    def to_compact(self):
        return {
            "claim": self.claim[:120],
            "chi": self.static_chi,
            "verdict": self.verdict,
            "gradient": self.gradient,
            "zeros": self.zero_channels,
            "weakest": self.weakest_channels,
            "strongest": self.strongest_channels,
            "fruit_score": self.fruit_output.fruit_score,
            "dominant_fruits": self.fruit_output.dominant_fruits[:3],
        }
