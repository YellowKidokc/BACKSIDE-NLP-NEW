import os
import shutil

# Paths
source = r'\\192.168.1.177\Desktop\DAVID WEBPAGES'
dest_base = r'\\192.168.1.177\Desktop\Gemini\'s web pages'

# Mapping Logic: (Source Folder/Keyword -> Destination Subfolder)
mapping = {
    # THO - Theophysics
    'THO_Theophysics/THO_Genesis_to_Quantum': ['genesis-to-quantum', 'GTQ_Genesis-to-Quantum', 'gtq-'],
    'THO_Theophysics/THO_The_Convergence_Logic': ['convergence', 'CVS_', 'CV1_', 'convergence-'],
    'THO_Theophysics/THO_Master_Equation_Architecture': ['Master EQ', 'MEQ_', 'the-same-equation', 'master_equation_unified'],

    # PHY - Physics
    'PHY_Physics/PHY_Quantum_Mechanics_Logic': ['PHY_Physics-Quantum', 'quantum-'],
    'PHY_Physics/PHY_Relativity_Noether_Symmetry': ['blue/', 'formal-papers', 'FPR_'],
    'PHY_Physics/PHY_Consciousness_Field_Research': ['consciousness', 'CON_'],

    # THE - Theology
    'THE_Theology/THE_Salvation_Algorithm_Grace': ['SAL_', 'salvation-algorithm', 'why-grace-from-outside'],
    'THE_Theology/THE_Character_of_God': ['character-of-god', 'character-of-adversary', 'JAS_', 'THO_Theology-General'],
    'THE_Theology/THE_Biblical_Studies_Complexity': ['BIB_', 'Biblical Complexity'],

    # APP - Applied
    'APP_Applied/APP_Moral_Decline_America': ['moral-decline', 'MDA_'],
    'APP_Applied/APP_Architecture_of_Debt': ['AOD_'],
    'APP_Applied/APP_Spiritual_Warfare_Applied': ['WAR_', 'the-attack-surface', 'the-24-anti-properties']
}

print("Starting Canonical Sort...")

moved_count = 0
already_moved = set() # To ensure no duplication

# Walk through the destination mapping
for dest_sub, keywords in mapping.items():
    dest_path = os.path.join(dest_base, dest_sub.replace('/', '\\'))
    
    # Scan DAVID WEBPAGES for matches
    for root, dirs, files in os.walk(source):
        # Skip the snippet mess and unknown review folders
        if any(x in root for x in ['_SNIPPET_MESS', '_UNKNOWN_FOR_REVIEW', 'Gemini']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                # Check if file or its parent folder matches keywords
                match = False
                for kw in keywords:
                    if kw.lower() in file.lower() or kw.lower() in root.lower():
                        match = True
                        break
                
                if match and file not in already_moved:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_path, file)
                    
                    try:
                        shutil.copy2(src_file, dest_file)
                        already_moved.add(file)
                        moved_count += 1
                        if moved_count % 50 == 0:
                            print(f"Sorted {moved_count} canonical files...")
                    except Exception as e:
                        print(f"Error copying {file}: {e}")

print(f"\n--- SORT COMPLETE ---")
print(f"Successfully sorted {moved_count} unique files into the 4-pillar structure.")
