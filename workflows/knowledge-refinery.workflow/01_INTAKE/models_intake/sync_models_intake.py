import os
import yaml
from pathlib import Path

MODELS_DIR = Path(r'X:\knowledge-refinery\BACKSIDE\MODELS\models')
INTAKE_DIR = Path(r'X:\knowledge-refinery\01_INTAKE\models_intake')
REGISTRY_FILE = INTAKE_DIR / 'model_intake_registry.yml'
SUBFOLDERS = ['ARCHIVE', 'CONFIG', 'ERROR', 'INPUT', 'LOGS', 'OUTPUT', 'REVIEW']

def sync():
    if not REGISTRY_FILE.exists():
        print(f"Error: Registry file not found at {REGISTRY_FILE}")
        return

    with open(REGISTRY_FILE, 'r') as f:
        registry = yaml.safe_load(f)

    existing_wrappers = {item['wrapper'] for item in registry.get('intake_mirrors', [])}
    
    # Get actual wrappers on disk
    actual_wrappers = [d.name for d in MODELS_DIR.iterdir() if d.is_dir()]
    
    new_wrappers = [w for w in actual_wrappers if w not in existing_wrappers]
    
    if not new_wrappers:
        print("Everything is already in sync.")
        return

    print(f"Found {len(new_wrappers)} new wrappers: {new_wrappers}")

    for wrapper in new_wrappers:
        intake_folder_name = f"{wrapper}_intake"
        intake_path = INTAKE_DIR / intake_folder_name
        
        print(f"Creating intake mirror: {intake_folder_name}")
        intake_path.mkdir(exist_ok=True)
        
        for sub in SUBFOLDERS:
            (intake_path / sub).mkdir(exist_ok=True)
            
        # Update registry memory (we'll write it once at the end)
        registry['intake_mirrors'].append({
            'wrapper': wrapper,
            'intake_folder': intake_folder_name
        })

    # Sort registry by wrapper name for cleanliness
    registry['intake_mirrors'].sort(key=lambda x: x['wrapper'])

    with open(REGISTRY_FILE, 'w') as f:
        yaml.dump(registry, f, sort_keys=False)
        
    print("Sync complete. Registry updated.")

if __name__ == "__main__":
    sync()
