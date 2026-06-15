"""FIS Actions — 8 filesystem operations with preview-approve pattern.

Every action follows the same flow:
  Pick items → Pick action → Pick target/name → Preview → Approve → Record

Actions:
  1. Combine    — bring related files/folders together
  2. Separate   — split messy folder into cleaner groups
  3. Rename     — clean identity
  4. Move       — relocate active file/folder
  5. Copy       — duplicate without changing original
  6. Archive    — remove from active area, preserve
  7. Delete Later — quarantine, not destroy
  8. Link / Hub — connect related things without merging
"""
import shutil
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ActionResult:
    """Result of a previewed or executed action."""
    action: str
    items: list[str]
    operations: list[dict]  # [{op: "move", src: ..., dst: ...}, ...]
    success: bool = False
    errors: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# --- Action Definitions (drives the GUI) ---

ACTION_DEFS = {
    "combine": {
        "label": "Combine",
        "purpose": "Bring related files/folders together",
        "icon": "📦",
        "options": [
            {"key": "combine_into", "label": "Combine into", "type": "choice",
             "choices": ["existing_folder", "new_folder"]},
            {"key": "folder_name", "label": "Folder name", "type": "text", "suggested": True},
            {"key": "conflict_rule", "label": "If name conflict", "type": "choice",
             "choices": ["keep_both", "rename_duplicates", "skip_duplicates"]},
            {"key": "originals", "label": "Originals", "type": "choice",
             "choices": ["move", "copy"]},
            {"key": "archive_empty", "label": "Archive empty folders after?", "type": "bool", "default": True},
        ],
    },
    "separate": {
        "label": "Separate",
        "purpose": "Split a messy folder into cleaner groups",
        "icon": "✂️",
        "options": [
            {"key": "separate_by", "label": "Separate by", "type": "choice",
             "choices": ["type", "domain", "tags", "date", "custom"]},
            {"key": "group_names", "label": "Group names", "type": "choice",
             "choices": ["auto", "custom"]},
            {"key": "destination", "label": "Destination", "type": "choice",
             "choices": ["inside_source", "new_location"]},
            {"key": "unknown_files", "label": "Unknown files", "type": "choice",
             "choices": ["leave_here", "send_to_review"]},
            {"key": "keep_original", "label": "Keep original folder?", "type": "choice",
             "choices": ["keep", "archive_if_empty"]},
        ],
    },
    "rename": {
        "label": "Rename",
        "purpose": "Clean identity",
        "icon": "🏷️",
        "options": [
            {"key": "preset", "label": "Name preset", "type": "choice",
             "choices": ["baseline", "short", "descriptive", "archive", "custom"]},
            {"key": "custom_name", "label": "Custom name", "type": "text", "conditional": "preset=custom"},
            {"key": "apply_to", "label": "Apply to", "type": "choice",
             "choices": ["file_only", "folder_only", "batch"]},
            {"key": "conflict_rule", "label": "If name exists", "type": "choice",
             "choices": ["add_version", "skip", "ask"]},
        ],
    },
    "move": {
        "label": "Move",
        "purpose": "Relocate active file/folder",
        "icon": "📁",
        "options": [
            {"key": "destination", "label": "Destination folder", "type": "folder_picker"},
            {"key": "reason", "label": "Reason/domain", "type": "text", "optional": True},
            {"key": "keep_sidecar", "label": "Keep .fcard metadata?", "type": "bool", "default": True},
            {"key": "conflict_rule", "label": "If same name exists", "type": "choice",
             "choices": ["rename", "never_overwrite", "skip"]},
            {"key": "create_missing", "label": "Create missing folder?", "type": "bool", "default": True},
        ],
    },
    "copy": {
        "label": "Copy",
        "purpose": "Duplicate without changing original",
        "icon": "📋",
        "options": [
            {"key": "destination", "label": "Copy to", "type": "folder_picker"},
            {"key": "copy_sidecar", "label": "Copy .fcard metadata?", "type": "bool", "default": True},
            {"key": "structure", "label": "Folder structure", "type": "choice",
             "choices": ["flat", "preserve_structure"]},
            {"key": "conflict_rule", "label": "If duplicate exists", "type": "choice",
             "choices": ["skip", "version", "replace_copy_only"]},
        ],
    },
    "archive": {
        "label": "Archive",
        "purpose": "Remove from active area but preserve",
        "icon": "🗄️",
        "options": [
            {"key": "destination", "label": "Archive destination", "type": "folder_picker"},
            {"key": "reason", "label": "Archive reason", "type": "choice",
             "choices": ["old", "finished", "duplicate", "inactive", "manual"]},
            {"key": "format", "label": "Archive format", "type": "choice",
             "choices": ["move_as_is", "zip_packet", "dated_folder"]},
            {"key": "keep_metadata", "label": "Keep searchable metadata?", "type": "bool", "default": True},
        ],
    },
    "delete_later": {
        "label": "Delete Later",
        "purpose": "Quarantine, not destroy",
        "icon": "🗑️",
        "options": [
            {"key": "reason", "label": "Reason", "type": "choice",
             "choices": ["duplicate", "junk", "temp", "failed_output", "unknown"]},
            {"key": "quarantine_folder", "label": "Quarantine folder", "type": "folder_picker"},
            {"key": "retention", "label": "Retention", "type": "choice",
             "choices": ["7_days", "30_days", "90_days", "manual_review"]},
            {"key": "hard_delete_ok", "label": "Allow hard delete later?", "type": "bool", "default": False},
        ],
    },
    "link": {
        "label": "Link / Hub",
        "purpose": "Connect related things without merging",
        "icon": "🔗",
        "options": [
            {"key": "hub_name", "label": "Hub name", "type": "text", "suggested": True},
            {"key": "hub_location", "label": "Hub location", "type": "folder_picker"},
            {"key": "link_type", "label": "Link type", "type": "choice",
             "choices": ["shortcut", "manifest_entry", "both"]},
            {"key": "hub_summary", "label": "Hub summary", "type": "choice",
             "choices": ["auto", "custom"]},
            {"key": "include_in_hub", "label": "Include", "type": "multi_choice",
             "choices": ["paths", "tags", "summaries", "counts"]},
        ],
    },
}


# --- Shared helpers ---

def _resolve_conflict(dst: Path, rule: str) -> Path:
    """Handle naming conflicts based on rule."""
    if not dst.exists():
        return dst
    if rule in ("skip", "skip_duplicates"):
        return None  # Signal to skip
    if rule in ("add_version", "rename_duplicates", "rename", "version", "keep_both"):
        stem = dst.stem
        ext = dst.suffix
        parent = dst.parent
        v = 1
        while True:
            candidate = parent / f"{stem}_v{v:02d}{ext}"
            if not candidate.exists():
                return candidate
            v += 1
    if rule in ("never_overwrite",):
        return None
    return dst  # Default: overwrite


def _record_action(result: ActionResult, log_dir: Path = None):
    """Write action to history log."""
    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "_LOGS"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"actions_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "action": result.action, "items": result.items,
            "operations": result.operations, "success": result.success,
            "errors": result.errors, "timestamp": result.timestamp,
        }) + "\n")


# --- Action executors ---

def preview_action(action: str, items: list[str], options: dict) -> ActionResult:
    """Preview any action — returns what WOULD happen without doing it."""
    func = _ACTION_FUNCS.get(action)
    if not func:
        return ActionResult(action=action, items=items, operations=[],
                           errors=[f"Unknown action: {action}"])
    return func(items, options, dry_run=True)


def execute_action(action: str, items: list[str], options: dict) -> ActionResult:
    """Execute any action and record to history."""
    func = _ACTION_FUNCS.get(action)
    if not func:
        return ActionResult(action=action, items=items, operations=[],
                           errors=[f"Unknown action: {action}"])
    result = func(items, options, dry_run=False)
    _record_action(result)
    return result


def _combine(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Combine: bring related files/folders together."""
    ops = []
    errors = []
    target_name = opts.get("folder_name", "combined")
    conflict = opts.get("conflict_rule", "keep_both")
    mode = opts.get("originals", "move")

    # Determine target folder
    if opts.get("combine_into") == "existing_folder" and opts.get("destination"):
        target = Path(opts["destination"])
    else:
        # Create new folder next to first item
        first = Path(items[0])
        target = first.parent / target_name

    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        dst = target / src.name
        dst = _resolve_conflict(dst, conflict)
        if dst is None:
            ops.append({"op": "skip", "src": str(src), "reason": "conflict_skip"})
            continue
        op_type = "move" if mode == "move" else "copy"
        ops.append({"op": op_type, "src": str(src), "dst": str(dst)})
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)
            if mode == "move":
                shutil.move(str(src), str(dst))
            else:
                if src.is_dir():
                    shutil.copytree(str(src), str(dst))
                else:
                    shutil.copy2(str(src), str(dst))

    return ActionResult(action="combine", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _separate(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Separate: split folder contents into groups."""
    ops = []
    errors = []
    source = Path(items[0]) if items else None
    if not source or not source.is_dir():
        return ActionResult(action="separate", items=items, operations=[],
                           errors=["Source must be a folder"])

    separate_by = opts.get("separate_by", "type")
    dest_mode = opts.get("destination", "inside_source")
    dest_base = source if dest_mode == "inside_source" else Path(opts.get("destination_path", str(source)))

    for item in sorted(source.iterdir()):
        if item.name.startswith('.') or item.suffix == '.fcard':
            continue
        # Group by extension type
        if separate_by == "type":
            group = item.suffix.lstrip('.').lower() or "no_extension"
        elif separate_by == "domain":
            group = "unknown"  # Would read from .fcard manifest
        elif separate_by == "date":
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            group = mtime.strftime("%Y-%m")
        else:
            group = "unsorted"

        group_dir = dest_base / group
        dst = group_dir / item.name
        ops.append({"op": "move", "src": str(item), "dst": str(dst), "group": group})
        if not dry_run:
            group_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(dst))

    return ActionResult(action="separate", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _rename(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Rename: clean identity."""
    ops = []
    errors = []
    conflict = opts.get("conflict_rule", "add_version")
    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        # Get new name from preset or custom
        preset = opts.get("preset", "baseline")
        if preset == "custom":
            new_name = opts.get("custom_name", src.name)
        elif preset in ("baseline",):
            from fis.baseline import to_baseline
            new_name = to_baseline(src.name)
        else:
            # Presets come from the classification card rename_preview
            new_name = opts.get(f"preset_{preset}", src.name)

        dst = src.parent / new_name
        dst = _resolve_conflict(dst, conflict)
        if dst is None:
            ops.append({"op": "skip", "src": str(src), "reason": "conflict_skip"})
            continue
        ops.append({"op": "rename", "src": str(src), "dst": str(dst)})
        if not dry_run and str(src) != str(dst):
            src.rename(dst)

    return ActionResult(action="rename", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _move(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Move: relocate active file/folder."""
    ops, errors = [], []
    dest = Path(opts.get("destination", ""))
    conflict = opts.get("conflict_rule", "rename")
    if not dest:
        return ActionResult(action="move", items=items, operations=[], errors=["No destination"])
    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        dst = dest / src.name
        dst = _resolve_conflict(dst, conflict)
        if dst is None:
            ops.append({"op": "skip", "src": str(src)})
            continue
        ops.append({"op": "move", "src": str(src), "dst": str(dst)})
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
    return ActionResult(action="move", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _copy(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Copy: duplicate without changing original."""
    ops, errors = [], []
    dest = Path(opts.get("destination", ""))
    conflict = opts.get("conflict_rule", "skip")
    structure = opts.get("structure", "flat")
    if not dest:
        return ActionResult(action="copy", items=items, operations=[], errors=["No destination"])
    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        dst = dest / src.name
        dst = _resolve_conflict(dst, conflict)
        if dst is None:
            ops.append({"op": "skip", "src": str(src)})
            continue
        ops.append({"op": "copy", "src": str(src), "dst": str(dst)})
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(str(src), str(dst))
            else:
                shutil.copy2(str(src), str(dst))
    return ActionResult(action="copy", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _archive(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Archive: remove from active area but preserve."""
    ops, errors = [], []
    dest = Path(opts.get("destination", ""))
    reason = opts.get("reason", "manual")
    fmt = opts.get("format", "move_as_is")
    if not dest:
        return ActionResult(action="archive", items=items, operations=[], errors=["No destination"])

    if fmt == "dated_folder":
        dest = dest / datetime.now().strftime("%Y-%m-%d")
    elif fmt == "zip_packet":
        # Zip all items into one archive
        import zipfile
        zip_name = dest / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        ops.append({"op": "zip", "dst": str(zip_name), "items": items})
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(str(zip_name), 'w', zipfile.ZIP_DEFLATED) as zf:
                for item_path in items:
                    src = Path(item_path)
                    if src.is_file():
                        zf.write(str(src), src.name)
                    elif src.is_dir():
                        for f in src.rglob('*'):
                            if f.is_file():
                                zf.write(str(f), str(f.relative_to(src.parent)))
        return ActionResult(action="archive", items=items, operations=ops,
                           success=True, errors=errors)

    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        dst = dest / src.name
        ops.append({"op": "archive_move", "src": str(src), "dst": str(dst), "reason": reason})
        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
    return ActionResult(action="archive", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _delete_later(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Delete Later: quarantine, not destroy."""
    ops, errors = [], []
    quarantine = Path(opts.get("quarantine_folder", ""))
    reason = opts.get("reason", "unknown")
    retention = opts.get("retention", "30_days")
    if not quarantine:
        return ActionResult(action="delete_later", items=items, operations=[], errors=["No quarantine folder"])

    retention_days = {"7_days": 7, "30_days": 30, "90_days": 90, "manual_review": -1}
    days = retention_days.get(retention, 30)
    purge_date = (datetime.now() + timedelta(days=days)).isoformat() if days > 0 else "manual"

    for item_path in items:
        src = Path(item_path)
        if not src.exists():
            errors.append(f"Not found: {item_path}")
            continue
        dst = quarantine / src.name
        ops.append({"op": "quarantine", "src": str(src), "dst": str(dst),
                    "reason": reason, "purge_after": purge_date})
        if not dry_run:
            quarantine.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
    return ActionResult(action="delete_later", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


def _link(items: list[str], opts: dict, dry_run: bool) -> ActionResult:
    """Link / Hub: connect related things without merging."""
    ops, errors = [], []
    hub_name = opts.get("hub_name", "hub")
    hub_loc = Path(opts.get("hub_location", ""))
    link_type = opts.get("link_type", "manifest_entry")
    if not hub_loc:
        return ActionResult(action="link", items=items, operations=[], errors=["No hub location"])

    hub_dir = hub_loc / hub_name
    manifest_path = hub_dir / "_hub.fcard"

    hub_data = {
        "hub_name": hub_name,
        "created_at": datetime.now().isoformat(),
        "links": [],
    }
    for item_path in items:
        src = Path(item_path)
        entry = {"path": str(src), "name": src.name, "exists": src.exists()}
        hub_data["links"].append(entry)

        if link_type in ("shortcut", "both") and os.name == 'nt':
            lnk_path = hub_dir / f"{src.stem}.lnk"
            ops.append({"op": "shortcut", "src": str(src), "dst": str(lnk_path)})
        if link_type in ("manifest_entry", "both"):
            ops.append({"op": "manifest_link", "src": str(src), "hub": str(manifest_path)})

    if not dry_run:
        hub_dir.mkdir(parents=True, exist_ok=True)
        import yaml
        with open(manifest_path, 'w', encoding='utf-8') as f:
            yaml.dump(hub_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return ActionResult(action="link", items=items, operations=ops,
                       success=len(errors) == 0, errors=errors)


# --- Dispatch ---

_ACTION_FUNCS = {
    "combine": _combine,
    "separate": _separate,
    "rename": _rename,
    "move": _move,
    "copy": _copy,
    "archive": _archive,
    "delete_later": _delete_later,
    "link": _link,
}
