import sys
sys.path.insert(0, r'X:\apps\paper-intelligence-suite-python\06_TRUTH_ENGINE')
from truth_coherence_scanner import ClaimRecord
import dataclasses
fields = [f.name for f in dataclasses.fields(ClaimRecord)]
with open(r'X:\Backside\MDA\_LOGS\scanner_check.txt', 'w') as f:
    f.write(f"ClaimRecord fields: {fields}\n")
    f.write(f"paragraph_index present: {'paragraph_index' in fields}\n")
