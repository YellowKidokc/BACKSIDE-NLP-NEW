"""
Chi Computation Module - Coherence Time Series Analysis

Computes:
- Pi (Polis): Trust, Violence, Economic, SocialCapital domains
- Lambda (Logos): Cognitive, Information domains
- A (Anthropos): Family, Meaning, Psychological domains
- Chi (Total): Geometric mean of (Pi * A * Lambda)^(1/3)
- dChi/dt: Rate of change of coherence

Based on the Theophysics Master Equation:
  dChi/dt = G(t) - S(t) - E(t) + R(F) - L(t)
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class DomainData:
    """Data for a single domain (e.g., Trust, Family, etc.)."""
    name: str
    triad: str  # 'Pi', 'Lambda', or 'A'
    years: List[int] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    metrics: Dict[str, List[float]] = field(default_factory=dict)

    @property
    def composite(self) -> List[float]:
        """Compute composite score as mean of all metrics."""
        if not self.metrics:
            return self.values

        # Average across all metrics for each year
        n_years = len(next(iter(self.metrics.values())))
        composites = []
        for i in range(n_years):
            vals = [m[i] for m in self.metrics.values() if i < len(m)]
            if vals:
                composites.append(np.mean(vals))
            else:
                composites.append(0.0)
        return composites


@dataclass
class TriadScore:
    """Triad component score (Pi, Lambda, or A)."""
    name: str
    years: List[int]
    values: List[float]
    domains: List[str]

    @property
    def current_value(self) -> float:
        """Get most recent value."""
        return self.values[-1] if self.values else 0.0


@dataclass
class ChiTimeSeries:
    """Complete Chi time series data."""
    years: List[int]
    chi_values: List[float]
    pi_values: List[float]
    lambda_values: List[float]
    a_values: List[float]
    dchi_dt: List[float]

    # Thresholds
    C_CRIT: float = 0.35  # Critical threshold

    @property
    def current_chi(self) -> float:
        """Current Chi value."""
        return self.chi_values[-1] if self.chi_values else 0.0

    @property
    def current_dchi_dt(self) -> float:
        """Current rate of change."""
        return self.dchi_dt[-1] if self.dchi_dt else 0.0

    @property
    def inflection_year(self) -> Optional[int]:
        """Find year when dChi/dt crossed from positive to negative."""
        for i in range(1, len(self.dchi_dt)):
            if self.dchi_dt[i-1] > 0 and self.dchi_dt[i] < 0:
                return self.years[i]
        return None

    @property
    def collapse_year(self) -> Optional[int]:
        """Find year when Chi first dropped below C_CRIT."""
        for i, chi in enumerate(self.chi_values):
            if chi < self.C_CRIT:
                return self.years[i]
        return None

    @property
    def regime(self) -> str:
        """Determine current regime."""
        if self.current_chi < self.C_CRIT:
            return "COLLAPSE"
        elif self.current_dchi_dt < 0:
            return "DECLINING"
        else:
            return "STABLE"


class ChiComputer:
    """Computes Chi time series from domain data."""

    # Domain to Triad mapping
    DOMAIN_TRIAD_MAP = {
        'Trust': 'Pi',
        'Violence': 'Pi',
        'Economic': 'Pi',
        'SocialCapital': 'Pi',
        'Cognitive': 'Lambda',
        'Information': 'Lambda',
        'Family': 'A',
        'Meaning': 'A',
        'Psychological': 'A',
    }

    def __init__(self):
        self.domains: Dict[str, DomainData] = {}
        self.years: List[int] = []

    def add_domain(self, domain: DomainData) -> None:
        """Add a domain's data."""
        self.domains[domain.name] = domain
        if domain.years and not self.years:
            self.years = domain.years

    def compute_triad(self, triad_name: str) -> TriadScore:
        """Compute a triad component (Pi, Lambda, or A)."""
        domains_in_triad = [
            d for d in self.domains.values()
            if self.DOMAIN_TRIAD_MAP.get(d.name) == triad_name
        ]

        if not domains_in_triad:
            return TriadScore(
                name=triad_name,
                years=self.years,
                values=[0.0] * len(self.years),
                domains=[]
            )

        # Average composites across domains in this triad
        n_years = len(self.years)
        triad_values = []

        for i in range(n_years):
            vals = []
            for d in domains_in_triad:
                composite = d.composite
                if i < len(composite):
                    vals.append(composite[i])
            if vals:
                triad_values.append(np.mean(vals))
            else:
                triad_values.append(0.0)

        return TriadScore(
            name=triad_name,
            years=self.years,
            values=triad_values,
            domains=[d.name for d in domains_in_triad]
        )

    def compute_chi(self) -> ChiTimeSeries:
        """Compute the full Chi time series."""
        # Compute triad components
        pi = self.compute_triad('Pi')
        lambda_ = self.compute_triad('Lambda')
        a = self.compute_triad('A')

        # Compute Chi as geometric mean
        chi_values = []
        for i in range(len(self.years)):
            pi_val = pi.values[i] if i < len(pi.values) else 0.0
            lambda_val = lambda_.values[i] if i < len(lambda_.values) else 0.0
            a_val = a.values[i] if i < len(a.values) else 0.0

            # Geometric mean: if any component is 0, Chi is 0
            if pi_val > 0 and lambda_val > 0 and a_val > 0:
                chi = (pi_val * lambda_val * a_val) ** (1/3)
            else:
                chi = 0.0

            chi_values.append(chi)

        # Compute dChi/dt (simple finite difference)
        dchi_dt = [0.0]  # First point has no derivative
        for i in range(1, len(chi_values)):
            dt = self.years[i] - self.years[i-1]
            if dt > 0:
                dchi_dt.append((chi_values[i] - chi_values[i-1]) / dt)
            else:
                dchi_dt.append(0.0)

        return ChiTimeSeries(
            years=self.years,
            chi_values=chi_values,
            pi_values=pi.values,
            lambda_values=lambda_.values,
            a_values=a.values,
            dchi_dt=dchi_dt
        )

    def load_from_excel(self, excel_path: Path) -> bool:
        """Load domain data from Coherence_Analysis_Master Excel file."""
        try:
            import pandas as pd
        except ImportError:
            print("pandas required for Excel loading")
            return False

        if not excel_path.exists():
            print(f"Excel file not found: {excel_path}")
            return False

        try:
            # Read all sheets
            xl = pd.ExcelFile(excel_path)

            # Map sheet names to domain names
            sheet_domain_map = {
                '01_Trust_Data': 'Trust',
                '02_Family_Data': 'Family',
                '03_Violence_Data': 'Violence',
                '04_Meaning_Data': 'Meaning',
                '05_Economic_Data': 'Economic',
                '06_Cognitive_Data': 'Cognitive',
                '07_Information_Data': 'Information',
                '08_SocialCapital_Data': 'SocialCapital',
                '09_Psychological_Data': 'Psychological',
            }

            for sheet_name, domain_name in sheet_domain_map.items():
                if sheet_name in xl.sheet_names:
                    df = pd.read_excel(xl, sheet_name=sheet_name)

                    # Extract year column and metric columns
                    if 'Year' in df.columns:
                        years = df['Year'].tolist()
                        metrics = {}

                        for col in df.columns:
                            if col != 'Year' and not col.startswith('Unnamed'):
                                # Normalize values to 0-1 if needed
                                vals = df[col].tolist()
                                vals = [v if pd.notna(v) else 0.0 for v in vals]
                                metrics[col] = vals

                        domain = DomainData(
                            name=domain_name,
                            triad=self.DOMAIN_TRIAD_MAP.get(domain_name, 'Unknown'),
                            years=years,
                            metrics=metrics
                        )
                        self.add_domain(domain)

            return True

        except Exception as e:
            print(f"Error loading Excel: {e}")
            return False

    def generate_report(self, chi_series: ChiTimeSeries) -> str:
        """Generate a text report of Chi analysis."""
        lines = []

        lines.append("=" * 60)
        lines.append("CHI COHERENCE TIME SERIES ANALYSIS")
        lines.append("=" * 60)
        lines.append("")

        # Current state
        lines.append("CURRENT STATE:")
        lines.append(f"  Chi (Total):   {chi_series.current_chi:.3f}")
        lines.append(f"  Pi (Polis):    {chi_series.pi_values[-1]:.3f}")
        lines.append(f"  Lambda (Logos):{chi_series.lambda_values[-1]:.3f}")
        lines.append(f"  A (Anthropos): {chi_series.a_values[-1]:.3f}")
        lines.append(f"  dChi/dt:       {chi_series.current_dchi_dt:.4f}")
        lines.append(f"  Regime:        {chi_series.regime}")
        lines.append("")

        # Key events
        lines.append("KEY EVENTS:")
        if chi_series.inflection_year:
            lines.append(f"  Inflection (dChi/dt -> negative): {chi_series.inflection_year}")
        if chi_series.collapse_year:
            lines.append(f"  Collapse (Chi < {chi_series.C_CRIT}): {chi_series.collapse_year}")
        lines.append("")

        # Thresholds
        lines.append("THRESHOLDS:")
        lines.append(f"  Critical (C_crit): {chi_series.C_CRIT}")
        lines.append(f"  Current Chi vs C_crit: {chi_series.current_chi:.3f} vs {chi_series.C_CRIT}")
        if chi_series.current_chi < chi_series.C_CRIT:
            lines.append("  STATUS: BELOW CRITICAL THRESHOLD")
        else:
            lines.append("  STATUS: Above critical threshold")
        lines.append("")

        # Time series (last 10 years)
        lines.append("RECENT HISTORY (last 10 data points):")
        lines.append("  Year    Chi     Pi    Lambda    A     dChi/dt")
        lines.append("  " + "-" * 50)

        n = len(chi_series.years)
        start = max(0, n - 10)
        for i in range(start, n):
            y = chi_series.years[i]
            c = chi_series.chi_values[i]
            p = chi_series.pi_values[i]
            l = chi_series.lambda_values[i]
            a = chi_series.a_values[i]
            d = chi_series.dchi_dt[i]
            lines.append(f"  {y}    {c:.3f}  {p:.3f}   {l:.3f}   {a:.3f}   {d:+.4f}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """Test the Chi computation."""
    import sys

    # Create sample data for testing
    computer = ChiComputer()

    # Generate sample data (1960-2024)
    years = list(range(1960, 2025))

    # Simulated decline pattern (peak around 1968-1972, then decline)
    def generate_domain_values(peak_year, peak_value, decay_rate):
        values = []
        for y in years:
            if y <= peak_year:
                # Rising to peak
                progress = (y - 1960) / (peak_year - 1960)
                v = 0.5 + (peak_value - 0.5) * progress
            else:
                # Declining from peak
                years_since_peak = y - peak_year
                v = peak_value * np.exp(-decay_rate * years_since_peak)
            values.append(max(0.1, min(1.0, v)))
        return values

    # Add simulated domains
    domains = [
        ('Trust', 'Pi', 1970, 0.85, 0.015),
        ('Violence', 'Pi', 1965, 0.80, 0.010),
        ('Economic', 'Pi', 1972, 0.75, 0.012),
        ('SocialCapital', 'Pi', 1968, 0.82, 0.018),
        ('Cognitive', 'Lambda', 1970, 0.78, 0.020),
        ('Information', 'Lambda', 1968, 0.85, 0.025),
        ('Family', 'A', 1965, 0.88, 0.016),
        ('Meaning', 'A', 1968, 0.80, 0.014),
        ('Psychological', 'A', 1970, 0.75, 0.018),
    ]

    for name, triad, peak, peak_val, decay in domains:
        values = generate_domain_values(peak, peak_val, decay)
        domain = DomainData(
            name=name,
            triad=triad,
            years=years,
            values=values
        )
        computer.add_domain(domain)

    # Compute Chi
    chi_series = computer.compute_chi()

    # Generate report
    report = computer.generate_report(chi_series)
    print(report)

    # Save to file
    output_path = Path("O:/Theophysics_Backend/Python_Backend/Global_Analytics/chi_analysis.txt")
    output_path.write_text(report, encoding='utf-8')
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
