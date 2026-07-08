from __future__ import annotations

from html import escape

from .schemas import LosslessArtifact


def render_html(artifact: LosslessArtifact) -> str:
    grades = artifact.four_score_dashboard
    semantic_tags_json = artifact.model_dump_json(include={"master_equation_uuid", "address", "vector_string", "hash", "semantic_tags"}).replace("</", "<\\/")
    claim_rows = "\n".join(
        f"<tr id=\"block-{escape(item.block_id)}\" data-semantic-block-id=\"{escape(item.block_id)}\"><td>{escape(item.claim_id[:8])}</td><td>{escape(', '.join(item.domain_badges))}</td><td>{escape(item.surface_claim[:260])}</td></tr>"
        for item in artifact.claim_arch
    )
    tag_rows = "\n".join(
        f"<tr id=\"tag-{escape(item.tag_id)}\" data-semantic-tag-id=\"{escape(item.tag_id)}\" data-block-id=\"{escape(item.block_id or '')}\" data-chi-vars=\"{escape(','.join(item.chi_vars))}\"><td>{escape(item.tag_type)}</td><td>{escape(item.label[:180])}</td><td>{escape(','.join(item.chi_vars))}</td><td>{escape(item.block_id or '')}</td></tr>"
        for item in artifact.semantic_tags
    )
    gap_rows = "\n".join(
        f"<tr><td>{escape(name)}</td><td>{escape(gap.status)}</td><td>{escape(gap.repair_action)}</td></tr>"
        for name, gap in artifact.eight_gaps.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Lossless Context Snapshot</title>
  <meta name="master-equation-uuid" content="{escape(artifact.master_equation_uuid)}">
  <meta name="semantic-address" content="{escape(artifact.address)}">
  <meta name="semantic-vector" content="{escape(artifact.vector_string)}">
  <script type="application/json" id="semantic-tags-json">{semantic_tags_json}</script>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; color: #18212f; background: #f7f8fb; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 24px; }}
    h1, h2 {{ margin-bottom: 8px; }}
    code {{ background: #e9eef6; padding: 2px 5px; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 14px 0 28px; }}
    th, td {{ border: 1px solid #d5dbe7; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #eef2f8; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }}
    .metric {{ background: white; border: 1px solid #d5dbe7; padding: 12px; }}
    .address {{ word-break: break-word; background: white; border: 1px solid #d5dbe7; padding: 12px; }}
  </style>
</head>
<body data-master-equation-uuid="{escape(artifact.master_equation_uuid)}" data-address="{escape(artifact.address)}">
<!--
{escape(artifact.semantic_tag_markdown)}
-->
<main>
  <h1>Lossless Context Snapshot</h1>
  <p class="address"><strong>Master Equation UUID:</strong> <code>{escape(artifact.master_equation_uuid)}</code><br><strong>Address:</strong> <code>{escape(artifact.address)}</code><br><strong>Recovery:</strong> {escape(artifact.recovery_key)}</p>
  <div class="grid">
    <div class="metric"><strong>Academic</strong><br>{grades.Academic_Readiness.score} / {escape(grades.Academic_Readiness.grade)}</div>
    <div class="metric"><strong>Coherence</strong><br>{grades.Framework_Coherence.score} / {escape(grades.Framework_Coherence.grade)}</div>
    <div class="metric"><strong>Public</strong><br>{grades.Public_Communication.score} / {escape(grades.Public_Communication.grade)}</div>
    <div class="metric"><strong>Risk</strong><br>{grades.Risk.score} / {escape(grades.Risk.grade)}</div>
  </div>
  <h2>Spine</h2>
  <ol>{"".join(f"<li>{escape(row)}</li>" for row in artifact.spine[:20])}</ol>
  <h2>Claims</h2>
  <table><tr><th>ID</th><th>Domains</th><th>Surface Claim</th></tr>{claim_rows}</table>
  <h2>Semantic Tags</h2>
  <table><tr><th>Type</th><th>Label</th><th>Chi Vars</th><th>Block Anchor</th></tr>{tag_rows}</table>
  <h2>Eight Gaps</h2>
  <table><tr><th>Gap</th><th>Status</th><th>Repair</th></tr>{gap_rows}</table>
</main>
</body>
</html>
"""
