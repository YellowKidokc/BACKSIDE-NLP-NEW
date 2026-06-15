# Lane 3 — PySide6 GUI Backend / Status Contract

Author: claude-code-worker-3
Date: 2026-05-13
Scope: define the read-only contract the PySide6 GUI uses to call pipeline scripts and parse their results. No production HTML is touched.

The GUI is a window over the workflow packet, not a second implementation. It launches scripts by `subprocess.Popen`, parses the JSON they emit to `OUTPUT/`, tails log files in `LOGS/`, and shows review artifacts from `REVIEW/`. It must never embed component-parsing logic of its own.

---

## 1. Process interface (every script the GUI launches)

The GUI launches each script as a child process. The script-to-GUI contract is identical for every command:

| Channel | Purpose | Rule |
|---|---|---|
| argv | Inputs | Only flags listed in this doc; no positional args. |
| cwd | Working dir | Always the workflow packet root (the dir containing `SCRIPTS/`, `CONFIG/`, `OUTPUT/`). |
| env | Side data | None required. `PYTHONIOENCODING=utf-8` is set by the GUI. |
| stdout | Human log | One line per file or one summary line per phase. GUI shows in Run Console. |
| stderr | Error log | Used only for genuine errors. GUI surfaces in Error pane. |
| Exit code | Outcome | `0` success, `2` partial (some files failed but report written), `1` hard fail (no report). |
| `OUTPUT/*.json` | Structured report | Written atomically (tmp file + rename). GUI reads after process exit. |
| `LOGS/<command>-<utc>.log` | Audit trail | Optional but recommended. GUI shows as link. |

### Atomicity rule

A run is "done" only when the process exits AND the declared `--out` JSON file exists. The GUI should treat any earlier `OUTPUT/*.json` as stale.

### Writes rule (non-negotiable)

| Command | Default | With `--apply` |
|---|---|---|
| `inventory` | reads HTML, writes only `--out` JSON | n/a (no write mode) |
| `extract` | reads HTML, writes copies into `--out` dir | n/a |
| `verify` | reads HTML, writes only `--out` JSON | n/a |
| `replace` | reads HTML, writes nothing | writes `<file>.bak` next to original, then overwrites original |

`replace --apply` is the only path that mutates production HTML. The GUI must require an explicit per-run confirmation before passing `--apply`.

---

## 2. Command catalog

These four commands are the current contract surface. Imported scripts (`label_gtq_sections`, `wire_navigation`, etc.) are NOT yet GUI-callable — see Section 7.

### 2.1 `component_operator.py inventory`

```
python SCRIPTS/component_operator.py inventory --root <path> --out <path>
```

| Flag | Required | Notes |
|---|---|---|
| `--root` | yes | File or directory. Recursive over `*.html`/`*.htm`. |
| `--out` | yes | JSON output path. Parent dir auto-created. |

Output schema → Section 3.1.

### 2.2 `component_operator.py extract`

```
python SCRIPTS/component_operator.py extract --root <path> --component <type:name> --out <dir>
```

| Flag | Required | Notes |
|---|---|---|
| `--root` | yes | Source root. |
| `--component` | yes | `type:name` (e.g. `sidebar:sidebar-toc`). Worker validates format. |
| `--out` | yes | Output **directory**. One file per source page that contained the component. |

Output filename pattern: `{rel_path_joined_with_double_underscore}.{type}.{name}.html`. The GUI Review Pane can list this directory directly.

This command does not emit a JSON report. Stdout prints `Extracted N copies …`. The GUI should count files in `--out` after exit to populate the inspector. **Gap:** no machine-readable summary. See Section 7 → IMP-2.

### 2.3 `component_operator.py verify`

```
python SCRIPTS/component_operator.py verify --root <path> --out <path>
```

Currently a thin alias for `inventory` (same schema). Kept separate so the contract can diverge later (verify can grow stricter rules without breaking inventory consumers).

### 2.4 `component_operator.py replace`

```
python SCRIPTS/component_operator.py replace --root <path> --component <type:name> --template <path> [--apply]
```

| Flag | Required | Notes |
|---|---|---|
| `--root` | yes | Source root. |
| `--component` | yes | `type:name`. |
| `--template` | yes | HTML file containing replacement block, including the BEGIN/END marker pair. |
| `--apply` | no | Default = dry run. When set, writes `.bak` and overwrites original. |

Output: stdout lines `DRY-RUN would replace …` or `APPLIED <path> backup=<bak>`. **Gap:** no JSON diff report; the GUI cannot show per-file before/after in dry-run mode. See Section 7 → IMP-1.

---

## 3. JSON schemas

Schemas are described in TypeScript-style notation; the actual encoding is plain JSON (UTF-8, indent=2).

### 3.1 `inventory.json` / `verify.json` (current shape, observed in `OUTPUT/k-production-ready.inventory.json`)

```ts
type FileStatus = "PASS" | "REVIEW";  // see Section 4 — recommended to expand

interface ComponentSpan {
  component_type: string;     // e.g. "sidebar"
  name: string;               // e.g. "sidebar-toc"
  start: number;              // byte offset of BEGIN marker
  end: number | null;         // byte offset of END marker, null if unmatched
  matched: boolean;
  key: string;                // "{component_type}:{name}", derived
}

interface FileInventory {
  path: string;               // path relative to --root if root is a dir
  page_meta: Record<string, string>;  // parsed PAGE_META block; {} if absent
  begin_count: number;        // total BEGIN markers found
  end_count: number;          // total END markers found
  data_component_count: number;  // count of data-component= attributes
  matched_count: number;      // BEGIN/END pairs successfully matched
  unmatched_begins: string[]; // keys still on the parse stack
  unmatched_ends: string[];   // keys that had no open BEGIN
  duplicates: string[];       // keys appearing more than once
  components: ComponentSpan[];
  status: FileStatus;
}

interface InventoryReport {
  generated_at: string;       // ISO8601 local time, no tz suffix
  root: string;               // absolute path as supplied to --root
  file_count: number;
  review_count: number;       // files where status != "PASS"
  files: FileInventory[];
}
```

### 3.2 Recommended additions (non-breaking)

These keys SHOULD be added by `component_operator.py` to make the GUI useful. None remove or rename existing keys:

```ts
interface FileInventory {
  // ...existing fields...
  reason_codes: string[];     // see Section 4; empty when status == "PASS"
  size_bytes: number;
  mtime: string;              // ISO8601
}

interface InventoryReport {
  // ...existing fields...
  schema_version: "1.0";      // bump on breaking change
  command: "inventory" | "verify";
  exit_code: 0 | 2 | 1;
  duration_ms: number;
  counts_by_status: Record<FileStatus, number>;
  counts_by_reason: Record<string, number>;
}
```

### 3.3 `extract.json` (proposed, currently missing)

```ts
interface ExtractResult {
  path: string;               // source file
  out_file: string;           // path written
  bytes: number;
}

interface ExtractReport {
  schema_version: "1.0";
  generated_at: string;
  command: "extract";
  root: string;
  component: string;          // "type:name"
  out_dir: string;
  exit_code: 0 | 2 | 1;
  duration_ms: number;
  match_count: number;
  miss_count: number;         // files scanned without that component
  results: ExtractResult[];
}
```

### 3.4 `replace.json` (proposed, currently missing — high priority)

```ts
interface ReplaceFileResult {
  path: string;
  component: string;
  would_change: boolean;
  applied: boolean;           // false in dry-run, true after --apply
  backup: string | null;      // path to .bak when applied
  before_hash: string;        // sha256 of original
  after_hash: string | null;  // sha256 after replace; null in dry-run
  diff_lines: { added: number; removed: number };
}

interface ReplaceReport {
  schema_version: "1.0";
  generated_at: string;
  command: "replace";
  root: string;
  component: string;
  template: string;
  apply: boolean;
  exit_code: 0 | 2 | 1;
  duration_ms: number;
  changed_count: number;
  results: ReplaceFileResult[];
}
```

The GUI's approve/apply gate depends on this report. Without it, dry-run is opaque.

---

## 4. File status model

Current `status` is `"PASS"` or `"REVIEW"`. `REVIEW` is overloaded: a file with zero markers and a file with a broken marker pair both land there. Worker 1's inventory of `K-Production-Ready/` shows 35/35 in `REVIEW`, all because the files are simply unmarked — that is a different problem from a malformed marker.

Recommended model:

| Status | Meaning | Reason codes (≥0 per file) |
|---|---|---|
| `PASS` | Has PAGE_META, all BEGIN/END matched, no duplicates, ≥1 component. | (none) |
| `UNMARKED` | Zero BEGIN markers found. Not broken, just not yet processed. | `NO_MARKERS` |
| `PARTIAL` | Has some markers but PAGE_META missing or component coverage thin. | `MISSING_PAGE_META`, `LOW_COMPONENT_COUNT` |
| `BROKEN` | Marker structure is invalid. | `UNMATCHED_BEGIN`, `UNMATCHED_END`, `DUPLICATE_KEY`, `NESTED_MISMATCH` |

The GUI's Pipeline Board lanes map directly to status:

| Lane | Statuses shown |
|---|---|
| Intake | `UNMARKED` |
| Inventory | `PARTIAL` |
| Error | `BROKEN` |
| Output | `PASS` |

This split is also what enables Worker 2's Phase 2 injection plan to filter files cleanly.

---

## 5. GUI ↔ backend state machine

```
                  ┌─────────────┐
                  │  IDLE       │
                  └─────┬───────┘
                        │ user clicks "Run Inventory"
                        ▼
                  ┌─────────────┐
                  │  LAUNCHING  │  GUI builds argv, opens log file
                  └─────┬───────┘
                        ▼
                  ┌─────────────┐
                  │  RUNNING    │  child process alive; GUI tails stdout
                  └─────┬───────┘
                        │ child exit
                        ▼
                  ┌─────────────┐
                  │  PARSING    │  GUI reads --out JSON
                  └──┬────────┬─┘
              exit=0│        │exit=1 or JSON missing
                    ▼        ▼
              ┌────────┐ ┌────────┐
              │ READY  │ │ FAILED │  GUI surfaces stderr in Error pane
              └────┬───┘ └────────┘
                   │ exit=2 → READY_WITH_ERRORS (show per-file errors)
                   ▼
              user reviews → IDLE
```

Transitions are GUI-side; the backend just emits exit codes and JSON.

---

## 6. Run Console / Logs / Review wiring

| Pane | Source |
|---|---|
| Source Tree | `CONFIG/source_roots.json` (`master_html_root`, `completed_marked_files`) |
| Pipeline Board | Latest `OUTPUT/*inventory*.json` grouped by `status` |
| Component Inspector | `files[i].components[]` for selected row |
| Run Console (stdout) | Tailed live from child process |
| Error Pane (stderr) | Tailed live; also `files[i]` where status ∈ {BROKEN, PARTIAL} |
| Review Pane | Directory listing of `REVIEW/` and `--out` dir for extract |
| Approve/Apply | Only enabled if `ReplaceReport.results[*].would_change` and user has clicked "Promote dry-run" |

Log file naming: `LOGS/{command}-{utc_yyyymmddThhmmss}.log` (e.g. `LOGS/inventory-20260513T180545Z.log`). The GUI passes this path to the script via env `PIPELINE_LOG_FILE` so each script can tee. Until scripts honor that, the GUI captures stdout/stderr itself.

---

## 7. Gaps and follow-up items for Codex

| ID | Item | Severity |
|---|---|---|
| IMP-1 | `replace` emits no JSON report; dry-run is unreviewable in the GUI. Need `replace.json` per Section 3.4. | high |
| IMP-2 | `extract` emits no JSON report. Need `extract.json` per Section 3.3. | medium |
| IMP-3 | `status` enum is binary; needs `UNMARKED`/`PARTIAL`/`BROKEN`/`PASS` + `reason_codes`. See Section 4. | high |
| IMP-4 | `--log` flag honoring `PIPELINE_LOG_FILE`. Today the GUI must capture stdout itself. | low |
| IMP-5 | Imported scripts (`label_gtq_sections`, `wire_navigation`, `wire_media`, `series_polish`) are not in the contract. Each needs an inventory-style JSON report and a dry-run mode before the GUI can call them. | high |
| IMP-6 | `inventory.root` is echoed verbatim from `--root`; if the user passes a relative path the GUI cannot resolve it later. Recommend the script normalize to absolute. | low |
| IMP-7 | No schema_version field. First breaking change will break the GUI silently. | medium |

These are recommendations, not blockers — the existing inventory/verify JSON is sufficient for the first GUI milestone (read-only Pipeline Board + Component Inspector). Replace and Extract panes are blocked on IMP-1/IMP-2.

---

## 8. Open question for David

The replace backup model (`<file>.bak` sibling) lives in the same folder as production HTML. Under Kimi's authority over `Master HTMl/`, is that acceptable, or should backups go to `ARCHIVE/<utc>/<original-rel-path>`? Default answer below if no decision is recorded:

> Default: route backups to `ARCHIVE/<utc>/` to keep production folders clean. CLAUDE.md says "every delete is a move to `_ARCHIVE/`" — extending that to overwrites is consistent.

This is a Kimi authority decision; defer to her if she has an opinion before Codex changes the script.
