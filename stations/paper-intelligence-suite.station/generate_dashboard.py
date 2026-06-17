#!/usr/bin/env python3
"""
generate_dashboard.py — Paper Intelligence Dashboard Generator
Reads a snapshot JSON from the NLP pipeline and produces a self-contained
HTML dashboard with Chart.js visualizations.

Usage:
  python generate_dashboard.py snapshot.json
  python generate_dashboard.py snapshot.json --out dashboards/
  python generate_dashboard.py --batch snapshots/
"""
import json, sys, argparse, html as html_mod
from pathlib import Path
from datetime import datetime

def safe(val, default="—"):
    if val is None or val == "": return default
    if isinstance(val, float): return f"{val:.3f}" if val < 10 else f"{val:.1f}"
    return str(val)

def pct_color(val):
    if val >= 70: return "#4ade80"
    if val >= 40: return "#fb923c"
    return "#f87171"

def grade_color(g):
    g = str(g).upper()
    if g.startswith("A"): return "#4ade80"
    if g.startswith("B"): return "#38bdf8"
    if g.startswith("C"): return "#fb923c"
    return "#f87171"
