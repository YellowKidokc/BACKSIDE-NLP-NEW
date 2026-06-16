"""
Theophysics Toolkit Manager
- Backup/restore golden master
- Deploy to new locations
- Version control
"""
import os
import shutil
import zipfile
import datetime
from pathlib import Path

# Paths
TOOLKIT_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = TOOLKIT_ROOT.parent.parent
BACKUP_DIR = VAULT_ROOT / "Theophysics_Backend" / "Backups"
MASTER_ZIP = VAULT_ROOT / "Global_Analytics_MASTER_v1.zip"

def backup(version_tag=None):
    """Create timestamped backup of Global_Analytics"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = f"_{version_tag}" if version_tag else ""
    zip_name = f"Global_Analytics_{ts}{tag}.zip"
    zip_path = BACKUP_DIR / zip_name
    
    source = VAULT_ROOT / "Global_Analytics"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source):
            # Skip __pycache__ and .git
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', '.obsidian')]
            for f in files:
                fp = Path(root) / f
                arcname = fp.relative_to(source)
                zf.write(fp, arcname)
    
    print(f"[OK] Backup created: {zip_path}")
    print(f"     Size: {zip_path.stat().st_size / 1024:.1f} KB")
    return zip_path

def restore(zip_path=None, target_dir=None):
    """Restore from backup zip"""
    zip_path = Path(zip_path) if zip_path else MASTER_ZIP
    target = Path(target_dir) if target_dir else VAULT_ROOT / "Global_Analytics_RESTORED"
    
    if not zip_path.exists():
        print(f"[ERROR] Zip not found: {zip_path}")
        return None
    
    target.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(target)
    
    print(f"[OK] Restored to: {target}")
    return target

def deploy(target_dir):
    """Deploy fresh copy of toolkit to new location"""
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)
    
    source = VAULT_ROOT / "Global_Analytics"
    
    # Copy everything except data files
    for item in source.iterdir():
        if item.name in ('Data', 'Reports', '__pycache__'):
            continue
        dest = target / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    
    # Create empty Data and Reports dirs
    (target / "BreakthroughVaultToolkit_v2" / "Data").mkdir(exist_ok=True)
    (target / "BreakthroughVaultToolkit_v2" / "Reports").mkdir(exist_ok=True)
    
    print(f"[OK] Deployed to: {target}")
    return target

def list_backups():
    """List all available backups"""
    if not BACKUP_DIR.exists():
        print("No backups found.")
        return []
    
    zips = sorted(BACKUP_DIR.glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"Found {len(zips)} backups:")
    for z in zips:
        size = z.stat().st_size / 1024
        mtime = datetime.datetime.fromtimestamp(z.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {z.name} ({size:.1f} KB) - {mtime}")
    
    return zips

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Theophysics Toolkit Manager")
    ap.add_argument("action", choices=["backup", "restore", "deploy", "list"])
    ap.add_argument("--tag", help="Version tag for backup")
    ap.add_argument("--zip", help="Zip path for restore")
    ap.add_argument("--target", help="Target directory for restore/deploy")
    args = ap.parse_args()
    
    if args.action == "backup":
        backup(args.tag)
    elif args.action == "restore":
        restore(args.zip, args.target)
    elif args.action == "deploy":
        if not args.target:
            print("--target required for deploy")
        else:
            deploy(args.target)
    elif args.action == "list":
        list_backups()
