
"""
grace_vault_manager.py (expanded)
Adds tabs:
- Scan
- Duplicates (with threshold slider 0–100% and suggested 75–90%)
- Auto-Linker (link style + jaccard threshold)
- Hubs
- Validate (SIS/LCS/SRI)
"""

import os, sys, subprocess
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "Data" / "coherence.db"
SCRIPTS = Path(__file__).resolve().parent

def run_cmd(cmd: list):
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(line, end="")
        proc.wait()
        return proc.returncode
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cli():
    import argparse
    ap = argparse.ArgumentParser(description="Grace Vault Manager")
    ap.add_argument("--vault", help="Path to Obsidian vault (root)")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--co", action="store_true")
    ap.add_argument("--hubs", action="store_true")
    ap.add_argument("--dupes", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--threshold", type=float, default=0.8, help="Duplicate sim threshold (0-1)")
    ap.add_argument("--min-jaccard", type=float, default=0.33, help="Auto-link min tag overlap (0-1)")
    ap.add_argument("--markdown-links", action="store_true")
    ap.add_argument("--write-yaml", action="store_true")
    args = ap.parse_args()

    db = Path(args.db)
    if args.auto:
        if not args.vault:
            ap.error("--auto requires --vault")
        run_cmd([sys.executable, str(SCRIPTS / "vault_refresh.py"), "--vault", args.vault, "--db", str(db)])
        run_cmd([sys.executable, str(SCRIPTS / "cooccurrence_analyzer.py"), "--db", str(db)])
        run_cmd([sys.executable, str(SCRIPTS / "duplicate_finder.py"), "--db", str(db), "--threshold", str(args.threshold)])
        run_cmd([sys.executable, str(SCRIPTS / "auto_linker.py"), "--db", str(db), "--min-jaccard", str(args.min_jaccard)] + (["--markdown-links"] if args.markdown_links else []) + (["--write-yaml"] if args.write_yaml else []))
        run_cmd([sys.executable, str(SCRIPTS / "validation_scaffold.py"), "--db", str(db)])
        return

    if args.scan:
        if not args.vault: ap.error("--scan requires --vault")
        run_cmd([sys.executable, str(SCRIPTS / "vault_refresh.py"), "--vault", args.vault, "--db", str(db)])
    if args.co:
        run_cmd([sys.executable, str(SCRIPTS / "cooccurrence_analyzer.py"), "--db", str(db)])
    if args.dupes:
        run_cmd([sys.executable, str(SCRIPTS / "duplicate_finder.py"), "--db", str(db), "--threshold", str(args.threshold)])
    if args.hubs:
        run_cmd([sys.executable, str(SCRIPTS / "concept_hub_generator.py"), "--db", str(db)])
    if args.validate:
        run_cmd([sys.executable, str(SCRIPTS / "validation_scaffold.py"), "--db", str(db)])

def gui():
    try:
        import PySimpleGUI as sg
    except ImportError:
        print("PySimpleGUI not installed. Use CLI mode or pip install PySimpleGUI.")
        sys.exit(1)

    sg.theme("SystemDefault")
    tab1 = [
        [sg.Text("Vault Path:"), sg.Input(key="-VAULT-"), sg.FolderBrowse()],
        [sg.Text("DB Path:"), sg.Input(default_text=str(DEFAULT_DB), key="-DB-"), sg.FileSaveAs(file_types=(("SQLite","*.db"),))],
        [sg.Button("Scan & Index"), sg.Button("Co-Mentions")]
    ]
    tab2 = [
        [sg.Text("Near-duplicate Threshold (suggest 75–90%)")],
        [sg.Slider(range=(0,100), default_value=80, orientation='h', key="-DUPTHR-"), sg.Text(" %")],
        [sg.Button("Find Duplicates"), sg.Text("Writes Data/duplicate_report.csv")]
    ]
    tab3 = [
        [sg.Text("Auto-Link Settings")],
        [sg.Text("Min Tag Overlap (Jaccard)"), sg.Slider(range=(0,100), default_value=33, orientation='h', key="-JACC-"), sg.Text("%")],
        [sg.Checkbox("Use Markdown links (instead of [[wikilinks]])", key="-MDLINK-")],
        [sg.Checkbox("Write links into notes (append YAML block)", key="-WRITEYAML-")],
        [sg.Button("Run Auto-Linker")]
    ]
    tab4 = [
        [sg.Button("Generate Concept Hubs")]
    ]
    tab5 = [
        [sg.Button("Run Validation (SIS/LCS/SRI)")]
    ]

    layout = [
        [sg.TabGroup([[
            sg.Tab("Scan", tab1),
            sg.Tab("Duplicates", tab2),
            sg.Tab("Auto-Linker", tab3),
            sg.Tab("Hubs", tab4),
            sg.Tab("Validate", tab5),
        ]])],
        [sg.Button("Run All"), sg.Exit()],
        [sg.Multiline(size=(100,20), key="-OUT-", autoscroll=True, reroute_stdout=True, reroute_stderr=True)]
    ]

    win = sg.Window("Grace Vault Manager (Phase 1+)", layout, finalize=True)
    while True:
        ev, vals = win.read()
        if ev in (sg.WIN_CLOSED, "Exit"):
            break
        vault = vals.get("-VAULT-")
        db = vals.get("-DB-")
        if ev == "Scan & Index":
            if not vault: print("Select a vault folder first."); continue
            run_cmd([sys.executable, str(SCRIPTS / "vault_refresh.py"), "--vault", vault, "--db", db])
            run_cmd([sys.executable, str(SCRIPTS / "cooccurrence_analyzer.py"), "--db", db])
        elif ev == "Co-Mentions":
            run_cmd([sys.executable, str(SCRIPTS / "cooccurrence_analyzer.py"), "--db", db])
        elif ev == "Find Duplicates":
            thr = float(vals["-DUPTHR-"]) / 100.0
            run_cmd([sys.executable, str(SCRIPTS / "duplicate_finder.py"), "--db", db, "--threshold", str(thr)])
        elif ev == "Run Auto-Linker":
            jthr = float(vals["-JACC-"]) / 100.0
            args = [sys.executable, str(SCRIPTS / "auto_linker.py"), "--db", db, "--min-jaccard", str(jthr)]
            if vals["-MDLINK-"]:
                args.append("--markdown-links")
            if vals["-WRITEYAML-"]:
                args.append("--write-yaml")
            run_cmd(args)
        elif ev == "Generate Concept Hubs":
            run_cmd([sys.executable, str(SCRIPTS / "concept_hub_generator.py"), "--db", db])
        elif ev == "Run Validation (SIS/LCS/SRI)":
            run_cmd([sys.executable, str(SCRIPTS / "validation_scaffold.py"), "--db", db])
        elif ev == "Run All":
            if not vault: print("Select a vault folder first."); continue
            thr = float(vals["-DUPTHR-"]) / 100.0
            jthr = float(vals["-JACC-"]) / 100.0
            run_cmd([sys.executable, str(SCRIPTS / "vault_refresh.py"), "--vault", vault, "--db", db])
            run_cmd([sys.executable, str(SCRIPTS / "cooccurrence_analyzer.py"), "--db", db])
            run_cmd([sys.executable, str(SCRIPTS / "duplicate_finder.py"), "--db", db, "--threshold", str(thr)])
            args = [sys.executable, str(SCRIPTS / "auto_linker.py"), "--db", db, "--min-jaccard", str(jthr)]
            if vals["-MDLINK-"]:
                args.append("--markdown-links")
            if vals["-WRITEYAML-"]:
                args.append("--write-yaml")
            run_cmd(args)
            run_cmd([sys.executable, str(SCRIPTS / "validation_scaffold.py"), "--db", db])
    win.close()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        cli()
    else:
        gui()
