from __future__ import annotations

import json
from pathlib import Path

from .schemas import LosslessArtifact


def write_outputs(artifact: LosslessArtifact, out_dir: Path) -> tuple[Path, Path]:
    from .pipeline import artifact_to_json
    from .render_html import render_html

    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{artifact.filename_safe_address}.json"
    html_path = out_dir / f"{artifact.filename_safe_address}.html"
    tags_md_path = out_dir / f"{artifact.filename_safe_address}.semantic-tags.md"
    tags_json_path = out_dir / f"{artifact.filename_safe_address}.semantic-tags.json"
    json_path.write_text(artifact_to_json(artifact), encoding="utf-8")
    html_path.write_text(render_html(artifact), encoding="utf-8")
    tags_md_path.write_text(artifact.semantic_tag_markdown, encoding="utf-8")
    tags_json_path.write_text(json.dumps([tag.model_dump(mode="json") for tag in artifact.semantic_tags], indent=2), encoding="utf-8")
    return json_path, html_path


def store_postgres(artifact: LosslessArtifact, dsn: str) -> None:
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("psycopg is required for --postgres-dsn storage") from exc

    payload = artifact.model_dump(mode="json")
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into lcc_documents (doc_id, vault_id, source_path)
                values (%s,%s,%s)
                on conflict (doc_id) do nothing
                """,
                (
                    artifact.ids.doc_id,
                    artifact.ids.vault_id,
                    artifact.compression_declaration.get("scope"),
                ),
            )
            cur.execute(
                """
                insert into lcc_audit_runs (run_id, vault_id, doc_id, note_version, content_hash)
                values (%s,%s,%s,%s,%s)
                on conflict (run_id) do nothing
                """,
                (
                    artifact.ids.run_id,
                    artifact.ids.vault_id,
                    artifact.ids.doc_id,
                    artifact.ids.note_version,
                    artifact.ids.content_hash,
                ),
            )
            cur.execute(
                """
                insert into lcc_audit_snapshots
                  (audit_snapshot_id, run_id, vault_id, doc_id, note_version, content_hash, address, vector, semantic_hash, master_equation_uuid, artifact)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                on conflict (audit_snapshot_id) do nothing
                """,
                (
                    artifact.ids.audit_snapshot_id,
                    artifact.ids.run_id,
                    artifact.ids.vault_id,
                    artifact.ids.doc_id,
                    artifact.ids.note_version,
                    artifact.ids.content_hash,
                    artifact.address,
                    json.dumps(artifact.semantic_vector),
                    artifact.hash,
                    artifact.master_equation_uuid,
                    json.dumps(payload),
                ),
            )
            for block in artifact.blocks:
                cur.execute(
                    """
                    insert into lcc_blocks
                      (block_id, audit_snapshot_id, doc_id, section_id, ordinal, block_type, content_hash, text, payload)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    on conflict (block_id) do nothing
                    """,
                    (
                        block.block_id,
                        artifact.ids.audit_snapshot_id,
                        artifact.ids.doc_id,
                        block.section_id,
                        block.ordinal,
                        block.block_type,
                        block.content_hash,
                        block.text,
                        json.dumps(block.model_dump(mode="json")),
                    ),
                )
            for tag in artifact.semantic_tags:
                cur.execute(
                    """
                    insert into lcc_semantic_tags
                      (tag_id, audit_snapshot_id, doc_id, block_id, tag_type, label, chi_vars, master_equation_uuid, payload)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    on conflict (tag_id) do nothing
                    """,
                    (
                        tag.tag_id,
                        artifact.ids.audit_snapshot_id,
                        artifact.ids.doc_id,
                        tag.block_id,
                        tag.tag_type,
                        tag.label,
                        tag.chi_vars,
                        tag.master_equation_uuid,
                        json.dumps(tag.model_dump(mode="json")),
                    ),
                )
        conn.commit()
