# NABLA Design Bible — Stub
# The full document (1398 lines) was uploaded this session from David's File_Naming_System.md.
# It contains the complete Nabla semantic addressing system design notes (30 rules).
# Source: \\dlowenas\HPWorkstation\Desktop\File Naming System.md
# 
# This stub exists to resolve M-9 from the Cowork review pass.
# Full file needs to be copied from the source above.
# Key rules summarized below for worker reference until the full file lands:

## Core Rules (from the 30 design notes)

1. Score the artifact, not the topic. A paper about chaos can be E=0 if the paper itself is clean.
2. Binary 0/3 orientation. No 1-2 scoring. Confidence is separate (0.00-1.00).
3. C=3 only when synthesis/integration/unification is the artifact's explicit dominant function.
4. E=3 only if the artifact itself is structurally noisy, fragmented, contradictory, corrupted.
5. Fixed tie-break order: E→C→G→K→M→T→R→F→S→Q.
6. The semantic address is NOT the grade. Address = identity. Grade = audit metadata.
7. Grades should not become permanent filenames because grades change after repair.
8. Confidence is not classification. 0/3 = address. 0.00-1.00 = confidence. Hamming distance = agreement.
9. Risk in semantic vector (R) = Relation/Bond. Risk in filing layer (R_file) = Risk level. Namespace them.
10. Do not collapse the four scores (Academic Readiness, Framework Coherence, Public Communication, Risk).
11. The unit is the claim, not the paper. Structured claim units scale; documents are containers.
12. Every object needs stable identity: vault_id, doc_id, note_version, content_hash, block_id, claim_id, etc.
13. Snapshots append, never overwrite. Provenance requires diff history.
14. Prompt versions are schema versions. A prompt change changes extraction behavior.
15. NLP does first-pass classification; LLM does reconstruction/review.
16. Obsidian = human surface. Postgres = audit memory. Python/NLP = extraction. LLM = reconstruction. HTML = review.
