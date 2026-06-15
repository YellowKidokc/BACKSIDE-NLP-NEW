"""
Dashboard Generator - Comprehensive Theophysics Analytics Report

Outputs all dashboards from the Global Analytics system plus signature metrics:
1. UTDGS (Universal Theory Defense Grading System)
2. Fruits of the Spirit (Structural Coherence Invariants)
3. Theory Comparison Metrics
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime
import json


# =============================================================================
# DASHBOARD CLASSES
# =============================================================================

@dataclass
class Dashboard:
    """Represents a dashboard file."""
    path: Path
    name: str
    title: str
    category: str
    size: int
    modified: datetime
    has_dataview: bool
    dataview_queries: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    sections: List[str] = field(default_factory=list)
    content_preview: str = ""


# =============================================================================
# UTDGS SCORING SYSTEM
# =============================================================================

@dataclass
class UTDGSScore:
    """Universal Theory Defense Grading System score."""
    objection_anticipation: float = 0.0  # 25%
    response_strength: float = 0.0       # 25%
    evidence_depth: float = 0.0          # 20%
    chain_completeness: float = 0.0      # 15%
    width_adequacy: float = 0.0          # 15%

    @property
    def total_score(self) -> float:
        return (
            self.objection_anticipation * 0.25 +
            self.response_strength * 0.25 +
            self.evidence_depth * 0.20 +
            self.chain_completeness * 0.15 +
            self.width_adequacy * 0.15
        ) * 100

    @property
    def grade(self) -> str:
        score = self.total_score
        if score >= 90: return "A+"
        if score >= 85: return "A"
        if score >= 80: return "A-"
        if score >= 75: return "B+"
        if score >= 70: return "B"
        if score >= 65: return "B-"
        if score >= 60: return "C+"
        if score >= 55: return "C"
        if score >= 50: return "C-"
        if score >= 45: return "D"
        return "F"


# =============================================================================
# FRUITS OF THE SPIRIT (STRUCTURAL COHERENCE INVARIANTS)
# =============================================================================

@dataclass
class FruitsScore:
    """Structural Coherence Invariants - The 12 Fruits."""
    grace: float = 0.0          # F1: Entropy absorption capacity
    hope: float = 0.0           # F2: Non-terminal failure states
    patience: float = 0.0       # F3: Iterative convergence
    faithfulness: float = 0.0   # F4: Structural fidelity under pressure
    self_control: float = 0.0   # F5: Defined boundaries and scope
    love: float = 0.0           # F6: Positive-sum orientation
    peace: float = 0.0          # F7: Internal consistency
    truth: float = 0.0          # F8: Signal fidelity to observation
    humility: float = 0.0       # F9: Update capacity
    goodness: float = 0.0       # F10: Generative surplus
    unity: float = 0.0          # F11: Integration without flattening
    joy: float = 0.0            # F12: Positive feedback resonance

    @property
    def total_score(self) -> float:
        return (
            self.grace + self.hope + self.patience + self.faithfulness +
            self.self_control + self.love + self.peace + self.truth +
            self.humility + self.goodness + self.unity + self.joy
        )

    def to_dict(self) -> Dict[str, float]:
        return {
            "F1-Grace": self.grace,
            "F2-Hope": self.hope,
            "F3-Patience": self.patience,
            "F4-Faithfulness": self.faithfulness,
            "F5-Self-Control": self.self_control,
            "F6-Love": self.love,
            "F7-Peace": self.peace,
            "F8-Truth": self.truth,
            "F9-Humility": self.humility,
            "F10-Goodness": self.goodness,
            "F11-Unity": self.unity,
            "F12-Joy": self.joy,
        }


# =============================================================================
# THEORY COMPARISON
# =============================================================================

@dataclass
class TheoryComparison:
    """Comparison of Theophysics vs other interpretations."""
    name: str
    problems_solved: int
    problems_total: int
    key_weaknesses: List[str]
    theophysics_advantage: str

    @property
    def score(self) -> str:
        return f"{self.problems_solved}/{self.problems_total}"


# =============================================================================
# MAIN GENERATOR CLASS
# =============================================================================

class DashboardGenerator:
    """Scans and outputs all dashboards with signature metrics."""

    DASHBOARD_PATTERNS = [
        "*Dashboard*.md", "*DASHBOARD*.md", "*_Index*.md", "*_Hub*.md",
        "*MOC*.md", "*MASTER*.md", "*Statistics*.md", "*Metrics*.md",
    ]

    # Theory comparison data (from BC7.1 and DOC-MWI-001)
    THEORY_COMPARISONS = [
        TheoryComparison(
            name="Copenhagen",
            problems_solved=1,
            problems_total=5,
            key_weaknesses=["Observer undefined", "No mechanism for collapse"],
            theophysics_advantage="Spirit provides definite collapse mechanism"
        ),
        TheoryComparison(
            name="Many-Worlds",
            problems_solved=0,
            problems_total=5,
            key_weaknesses=["No 'now'", "No Born rule", "Infinite entities", "No consciousness role", "Preferred basis"],
            theophysics_advantage="Finite mechanism, actual nowness, derived probability"
        ),
        TheoryComparison(
            name="GRW (Spontaneous Collapse)",
            problems_solved=2,
            problems_total=5,
            key_weaknesses=["Ad hoc parameters", "Untested"],
            theophysics_advantage="Collapse grounded in necessary Trinity structure"
        ),
        TheoryComparison(
            name="Penrose (Gravity-induced)",
            problems_solved=2,
            problems_total=5,
            key_weaknesses=["Speculative", "No consciousness integration"],
            theophysics_advantage="Consciousness participates in physics"
        ),
        TheoryComparison(
            name="IIT (Integrated Information)",
            problems_solved=3,
            problems_total=5,
            key_weaknesses=["No physics bridge", "Phi computation difficult"],
            theophysics_advantage="Full physics-consciousness integration"
        ),
    ]

    def __init__(self, base_path: Path, axioms_path: Optional[Path] = None):
        self.base_path = base_path
        self.axioms_path = axioms_path or Path(r"O:\_THEO\AXIOMS_MASTER\Axioms")
        self.dashboards: List[Dashboard] = []
        self.categories: Dict[str, List[Dashboard]] = {}
        self.utdgs_score: Optional[UTDGSScore] = None
        self.fruits_score: Optional[FruitsScore] = None

    def scan_all(self) -> int:
        """Scan for all dashboard files."""
        self.dashboards.clear()
        self.categories.clear()

        for pattern in self.DASHBOARD_PATTERNS:
            for md_file in self.base_path.rglob(pattern):
                if md_file.is_file():
                    dashboard = self._parse_dashboard(md_file)
                    if dashboard:
                        self.dashboards.append(dashboard)

        seen_paths: Set[Path] = set()
        unique_dashboards: List[Dashboard] = []
        for d in self.dashboards:
            if d.path not in seen_paths:
                seen_paths.add(d.path)
                unique_dashboards.append(d)
        self.dashboards = unique_dashboards
        self._categorize_dashboards()

        # Calculate signature metrics
        self._calculate_utdgs()
        self._calculate_fruits()

        return len(self.dashboards)

    def _parse_dashboard(self, file_path: Path) -> Optional[Dashboard]:
        """Parse a dashboard file and extract metadata."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return None

        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else file_path.stem

        rel_path = file_path.relative_to(self.base_path)
        parts = rel_path.parts
        category = parts[0] if parts else "Root"

        dataview_matches = re.findall(r'```dataview\n(.*?)```', content, re.DOTALL)
        has_dataview = len(dataview_matches) > 0

        links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

        stat = file_path.stat()

        return Dashboard(
            path=file_path,
            name=file_path.stem,
            title=title,
            category=category,
            size=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
            has_dataview=has_dataview,
            dataview_queries=dataview_matches,
            links=links[:20],
            sections=sections[:10],
            content_preview=content[:500].replace('\n', ' ')
        )

    def _categorize_dashboards(self) -> None:
        """Organize dashboards by category."""
        for d in self.dashboards:
            if d.category not in self.categories:
                self.categories[d.category] = []
            self.categories[d.category].append(d)

    def _calculate_utdgs(self) -> None:
        """Calculate UTDGS score from axiom files."""
        if not self.axioms_path.exists():
            self.utdgs_score = UTDGSScore()
            return

        total_files = 0
        objection_count = 0
        response_count = 0
        evidence_depth = 0
        chain_complete = 0

        objection_patterns = [
            r'objection', r'critic', r'challenge', r'problem', r'weakness',
            r'one might argue', r'could be argued', r'counter-argument'
        ]
        response_patterns = [
            r'resolves because', r'this fails because', r'therefore we see',
            r'the answer is', r'blocked', r'defense'
        ]
        evidence_patterns = [
            r'proof:', r'evidence:', r'empirical', r'testable', r'falsifiable',
            r'data shows', r'experiment'
        ]

        for md_file in self.axioms_path.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8').lower()
                total_files += 1

                for p in objection_patterns:
                    if re.search(p, content):
                        objection_count += 1
                        break

                for p in response_patterns:
                    if re.search(p, content):
                        response_count += 1
                        break

                for p in evidence_patterns:
                    if re.search(p, content):
                        evidence_depth += 1
                        break

                if 'logic chain' in content or 'defense grid' in content:
                    chain_complete += 1

            except Exception:
                continue

        if total_files > 0:
            self.utdgs_score = UTDGSScore(
                objection_anticipation=min(1.0, objection_count / total_files * 1.5),
                response_strength=min(1.0, response_count / total_files * 1.5),
                evidence_depth=min(1.0, evidence_depth / total_files * 1.5),
                chain_completeness=min(1.0, chain_complete / total_files * 2.0),
                width_adequacy=0.7  # Baseline for structured axiom system
            )
        else:
            self.utdgs_score = UTDGSScore()

    def _calculate_fruits(self) -> None:
        """Calculate Fruits of the Spirit score from axiom files."""
        if not self.axioms_path.exists():
            self.fruits_score = FruitsScore()
            return

        # Patterns for each fruit
        fruit_patterns = {
            'grace': [r'grace', r'mercy', r'forgive', r'restore', r'repair'],
            'hope': [r'hope', r'future', r'eschatolog', r'promise', r'resurrection'],
            'patience': [r'patience', r'iterative', r'convergence', r'process'],
            'faithfulness': [r'faithful', r'fidelity', r'consistent', r'reliable'],
            'self_control': [r'boundary', r'scope', r'limit', r'constraint', r'falsifiable'],
            'love': [r'love', r'positive.sum', r'coherence', r'unity'],
            'peace': [r'peace', r'shalom', r'consistent', r'non.contradict'],
            'truth': [r'truth', r'logos', r'fidelity', r'signal'],
            'humility': [r'update', r'revision', r'humility', r'learn'],
            'goodness': [r'goodness', r'generative', r'creative', r'produce'],
            'unity': [r'unity', r'trinity', r'integrat', r'unified'],
            'joy': [r'joy', r'resonance', r'positive feedback', r'flourish'],
        }

        scores = {k: 0.0 for k in fruit_patterns.keys()}
        total_files = 0

        for md_file in self.axioms_path.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8').lower()
                total_files += 1

                for fruit, patterns in fruit_patterns.items():
                    for p in patterns:
                        if re.search(p, content):
                            scores[fruit] += 1
                            break
            except Exception:
                continue

        if total_files > 0:
            self.fruits_score = FruitsScore(
                grace=min(1.0, scores['grace'] / total_files * 3),
                hope=min(1.0, scores['hope'] / total_files * 3),
                patience=min(1.0, scores['patience'] / total_files * 3),
                faithfulness=min(1.0, scores['faithfulness'] / total_files * 3),
                self_control=min(1.0, scores['self_control'] / total_files * 3),
                love=min(1.0, scores['love'] / total_files * 3),
                peace=min(1.0, scores['peace'] / total_files * 3),
                truth=min(1.0, scores['truth'] / total_files * 3),
                humility=min(1.0, scores['humility'] / total_files * 3),
                goodness=min(1.0, scores['goodness'] / total_files * 3),
                unity=min(1.0, scores['unity'] / total_files * 3),
                joy=min(1.0, scores['joy'] / total_files * 3),
            )
        else:
            self.fruits_score = FruitsScore()

    # =========================================================================
    # OUTPUT METHODS
    # =========================================================================

    def output_comprehensive_report(self) -> str:
        """Generate the full comprehensive report with all metrics."""
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append("THEOPHYSICS GLOBAL ANALYTICS REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Base Path: {self.base_path}")
        lines.append(f"Axioms Path: {self.axioms_path}")
        lines.append("")

        # =================================================================
        # SECTION 1: SIGNATURE METRICS
        # =================================================================
        lines.append("=" * 80)
        lines.append("SECTION 1: SIGNATURE METRICS")
        lines.append("=" * 80)
        lines.append("")

        # UTDGS Score
        lines.append("-" * 40)
        lines.append("UTDGS (Universal Theory Defense Grading System)")
        lines.append("-" * 40)
        if self.utdgs_score:
            lines.append(f"  Total Score: {self.utdgs_score.total_score:.1f}/100")
            lines.append(f"  Grade: {self.utdgs_score.grade}")
            lines.append("")
            lines.append("  Components:")
            lines.append(f"    Objection Anticipation (25%): {self.utdgs_score.objection_anticipation:.2%}")
            lines.append(f"    Response Strength (25%):      {self.utdgs_score.response_strength:.2%}")
            lines.append(f"    Evidence Depth (20%):         {self.utdgs_score.evidence_depth:.2%}")
            lines.append(f"    Chain Completeness (15%):     {self.utdgs_score.chain_completeness:.2%}")
            lines.append(f"    Width Adequacy (15%):         {self.utdgs_score.width_adequacy:.2%}")
        lines.append("")

        # Fruits Score
        lines.append("-" * 40)
        lines.append("FRUITS OF THE SPIRIT (Structural Coherence Invariants)")
        lines.append("-" * 40)
        if self.fruits_score:
            lines.append(f"  Total Score: {self.fruits_score.total_score:.2f}/12.00")
            lines.append("")
            lines.append("  Individual Fruits:")
            for name, value in self.fruits_score.to_dict().items():
                bar = "=" * int(value * 20)
                lines.append(f"    {name:<18} {value:.3f} [{bar:<20}]")
        lines.append("")

        # =================================================================
        # SECTION 2: THEORY COMPARISON
        # =================================================================
        lines.append("=" * 80)
        lines.append("SECTION 2: THEORY COMPARISON (Theophysics vs Alternatives)")
        lines.append("=" * 80)
        lines.append("")
        lines.append("| Theory                    | Score | Key Weaknesses                          |")
        lines.append("|---------------------------|-------|----------------------------------------|")
        for tc in self.THEORY_COMPARISONS:
            weaknesses = ", ".join(tc.key_weaknesses[:2])
            if len(tc.key_weaknesses) > 2:
                weaknesses += "..."
            lines.append(f"| {tc.name:<25} | {tc.score:<5} | {weaknesses:<40} |")
        lines.append("")
        lines.append("Theophysics Score: 5/5 (All problems addressed)")
        lines.append("")

        # =================================================================
        # SECTION 3: DASHBOARD INVENTORY
        # =================================================================
        lines.append("=" * 80)
        lines.append("SECTION 3: DASHBOARD INVENTORY")
        lines.append("=" * 80)
        lines.append("")

        total = len(self.dashboards)
        with_dataview = sum(1 for d in self.dashboards if d.has_dataview)
        total_links = sum(len(d.links) for d in self.dashboards)

        lines.append(f"Total Dashboards: {total}")
        lines.append(f"With Dataview Queries: {with_dataview}")
        lines.append(f"Total Internal Links: {total_links}")
        lines.append(f"Categories: {len(self.categories)}")
        lines.append("")

        for category, dashboards in sorted(self.categories.items()):
            lines.append(f"[{category}] ({len(dashboards)} dashboards)")
            for d in sorted(dashboards, key=lambda x: x.name)[:10]:  # First 10 per category
                dv = "[DV]" if d.has_dataview else "    "
                lines.append(f"  {dv} {d.name}")
            if len(dashboards) > 10:
                lines.append(f"  ... and {len(dashboards) - 10} more")
            lines.append("")

        # =================================================================
        # SECTION 4: THE 11 UNIVERSAL LAWS
        # =================================================================
        lines.append("=" * 80)
        lines.append("SECTION 4: THE 11 UNIVERSAL LAWS (Physics-Spiritual Correspondence)")
        lines.append("=" * 80)
        lines.append("")

        laws = [
            ("LAW 1", "Universal Gravitation -> Sin's Pull", "F = G(m1*m2)/r^2"),
            ("LAW 2", "Strong Nuclear Force -> Divine Unity", "V(r) = -g^2 * e^(-mr)/r"),
            ("LAW 3", "Electromagnetism -> Truth & Light", "c = 1/sqrt(e0*u0)"),
            ("LAW 4", "Entropy -> Universal Decay", "dS >= 0 (Second Law)"),
            ("LAW 5", "Light vs Darkness -> Truth vs Lies", "I = P/(4*pi*r^2)"),
            ("LAW 6", "Cause & Effect -> Sowing & Reaping", "F_reaction = -F_action"),
            ("LAW 7", "Relativity -> God's Eternal Perspective", "t' = t/sqrt(1-v^2/c^2)"),
            ("LAW 8", "Quantum-Spiritual Framework", "Theta = Q + U"),
            ("LAW 9", "Quantum Uncertainty -> Free Will", "dx*dp >= h/2"),
            ("LAW 10", "Fundamental Forces -> Spiritual Authority", "F_total = Sum(F_i)"),
            ("LAW 11", "Consciousness -> The Soul's Reality", "I = -Sum(p_i * log2(p_i))"),
        ]

        lines.append("| Law | Correspondence | Physical Form |")
        lines.append("|-----|---------------|---------------|")
        for law_id, desc, formula in laws:
            lines.append(f"| {law_id} | {desc} | {formula} |")
        lines.append("")

        # =================================================================
        # SECTION 5: MASTER EQUATION SUMMARY
        # =================================================================
        lines.append("=" * 80)
        lines.append("SECTION 5: THE MASTER EQUATION (LAW 12)")
        lines.append("=" * 80)
        lines.append("")
        lines.append("chi = integral(G * M * E * S * T * K * R * Q * F * C) dx dy dt dS_s")
        lines.append("")
        lines.append("Entropy Form:")
        lines.append("  dS/dt = Sum_i f(Delta_i) - R(Lambda)")
        lines.append("")
        lines.append("Where:")
        lines.append("  S = System Entropy (measurable chaos)")
        lines.append("  Delta_i = Deviation from design in domain i")
        lines.append("  f(Delta_i) = Entropy production function (nonlinear)")
        lines.append("  Lambda = Covenant strength (transcendent relationship)")
        lines.append("  R(Lambda) = Restoration/negentropy function (Grace)")
        lines.append("")
        lines.append("Dimensions:")
        lines.append("  dx, dy = Physical extension")
        lines.append("  dt = Time flow")
        lines.append("  dS_s = Soul condition")
        lines.append("")
        lines.append("Key Insight: R(Lambda) operates from OUTSIDE the closed system,")
        lines.append("providing the external negentropy required by the 2nd Law.")
        lines.append("")

        # Footer
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def output_all_formats(self, output_dir: Path) -> Dict[str, Path]:
        """Generate all output formats at once."""
        outputs = {}

        # Comprehensive report
        report_path = output_dir / "THEOPHYSICS_REPORT.txt"
        report_path.write_text(self.output_comprehensive_report(), encoding='utf-8')
        outputs['report'] = report_path

        # JSON data
        json_path = output_dir / "dashboard_data.json"
        json_path.write_text(self.output_json(), encoding='utf-8')
        outputs['json'] = json_path

        # Markdown index
        md_path = output_dir / "dashboard_index.md"
        md_path.write_text(self.output_markdown(), encoding='utf-8')
        outputs['markdown'] = md_path

        return outputs

    def output_json(self) -> str:
        """Generate JSON output."""
        data = {
            "generated": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "axioms_path": str(self.axioms_path),
            "signature_metrics": {
                "utdgs": {
                    "total_score": self.utdgs_score.total_score if self.utdgs_score else 0,
                    "grade": self.utdgs_score.grade if self.utdgs_score else "N/A",
                    "components": {
                        "objection_anticipation": self.utdgs_score.objection_anticipation if self.utdgs_score else 0,
                        "response_strength": self.utdgs_score.response_strength if self.utdgs_score else 0,
                        "evidence_depth": self.utdgs_score.evidence_depth if self.utdgs_score else 0,
                        "chain_completeness": self.utdgs_score.chain_completeness if self.utdgs_score else 0,
                        "width_adequacy": self.utdgs_score.width_adequacy if self.utdgs_score else 0,
                    }
                },
                "fruits": {
                    "total_score": self.fruits_score.total_score if self.fruits_score else 0,
                    "individual": self.fruits_score.to_dict() if self.fruits_score else {}
                }
            },
            "theory_comparisons": [
                {
                    "name": tc.name,
                    "score": tc.score,
                    "weaknesses": tc.key_weaknesses,
                    "theophysics_advantage": tc.theophysics_advantage
                }
                for tc in self.THEORY_COMPARISONS
            ],
            "dashboards": {
                "total": len(self.dashboards),
                "with_dataview": sum(1 for d in self.dashboards if d.has_dataview),
                "categories": {k: len(v) for k, v in self.categories.items()},
                "files": [
                    {
                        "name": d.name,
                        "path": str(d.path),
                        "has_dataview": d.has_dataview,
                        "links": len(d.links)
                    }
                    for d in self.dashboards
                ]
            }
        }
        return json.dumps(data, indent=2)

    def output_markdown(self) -> str:
        """Generate Markdown output."""
        lines = []
        lines.append("# Theophysics Global Analytics Report")
        lines.append("")
        lines.append(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Signature Metrics
        lines.append("## Signature Metrics")
        lines.append("")
        lines.append("### UTDGS Score")
        lines.append("")
        if self.utdgs_score:
            lines.append(f"**Total: {self.utdgs_score.total_score:.1f}/100 (Grade: {self.utdgs_score.grade})**")
            lines.append("")
            lines.append("| Component | Score |")
            lines.append("|-----------|-------|")
            lines.append(f"| Objection Anticipation | {self.utdgs_score.objection_anticipation:.1%} |")
            lines.append(f"| Response Strength | {self.utdgs_score.response_strength:.1%} |")
            lines.append(f"| Evidence Depth | {self.utdgs_score.evidence_depth:.1%} |")
            lines.append(f"| Chain Completeness | {self.utdgs_score.chain_completeness:.1%} |")
            lines.append(f"| Width Adequacy | {self.utdgs_score.width_adequacy:.1%} |")
        lines.append("")

        lines.append("### Fruits of the Spirit")
        lines.append("")
        if self.fruits_score:
            lines.append(f"**Total: {self.fruits_score.total_score:.2f}/12.00**")
            lines.append("")
            lines.append("| Fruit | Score |")
            lines.append("|-------|-------|")
            for name, value in self.fruits_score.to_dict().items():
                lines.append(f"| {name} | {value:.3f} |")
        lines.append("")

        # Theory Comparison
        lines.append("## Theory Comparison")
        lines.append("")
        lines.append("| Theory | Score | Theophysics Advantage |")
        lines.append("|--------|-------|----------------------|")
        for tc in self.THEORY_COMPARISONS:
            lines.append(f"| {tc.name} | {tc.score} | {tc.theophysics_advantage} |")
        lines.append("")

        # Dashboard Overview
        lines.append("## Dashboard Inventory")
        lines.append("")
        lines.append(f"| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Dashboards | {len(self.dashboards)} |")
        lines.append(f"| With Dataview | {sum(1 for d in self.dashboards if d.has_dataview)} |")
        lines.append(f"| Categories | {len(self.categories)} |")
        lines.append("")

        return "\n".join(lines)


def main():
    """Main entry point."""
    import argparse
    import sys

    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Generate Theophysics Analytics Report")
    parser.add_argument("--path", type=str,
                       default=r"O:\Theophysics_Backend\Python_Backend\Global_Analytics",
                       help="Base path to scan")
    parser.add_argument("--axioms", type=str,
                       default=r"O:\_THEO\AXIOMS_MASTER\Axioms",
                       help="Path to axioms folder")
    parser.add_argument("--output", type=str,
                       default=r"O:\Theophysics_Backend\Python_Backend\Global_Analytics",
                       help="Output directory")
    parser.add_argument("--all", action="store_true",
                       help="Generate all output formats")

    args = parser.parse_args()

    base_path = Path(args.path)
    axioms_path = Path(args.axioms)
    output_dir = Path(args.output)

    generator = DashboardGenerator(base_path, axioms_path)
    count = generator.scan_all()

    print(f"Found {count} dashboards.", file=sys.stderr)
    print(f"UTDGS Score: {generator.utdgs_score.total_score:.1f}/100 ({generator.utdgs_score.grade})", file=sys.stderr)
    print(f"Fruits Score: {generator.fruits_score.total_score:.2f}/12.00", file=sys.stderr)

    if args.all:
        outputs = generator.output_all_formats(output_dir)
        print(f"\nGenerated files:", file=sys.stderr)
        for name, path in outputs.items():
            print(f"  {name}: {path}", file=sys.stderr)
    else:
        print(generator.output_comprehensive_report())


if __name__ == "__main__":
    main()
