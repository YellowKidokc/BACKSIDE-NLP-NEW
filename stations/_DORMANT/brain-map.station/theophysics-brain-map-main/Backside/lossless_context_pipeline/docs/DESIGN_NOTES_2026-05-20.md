# Design Notes - What We Learned

These notes sit beside the Lossless Context Compression + Semantic Addressing Protocol as calibration guidance. They explain why the protocol exists and which edge failures the implementation must avoid.

## 1. Score the artifact, not the topic

Bad version:

```text
A document about entropy gets E=3.
A document about faith gets F=3.
A document about love gets R=3.
```

Correct version:

```text
Score what the document structurally is and how it functions.
Do not score only what it talks about.
```

A paper about chaos can be clean and coherent, so `E=0`. A legal contract about love can still be primarily binding, not emotional. A checklist about safety can be procedural, not experiential.

This rule prevents topic-tagging from pretending to be artifact classification.

## 2. Binary orientation solved the drift problem

The old `0-3` scale caused cross-model drift. Different models would agree a signal was present, but disagree on degree:

```text
Model A: K=1
Model B: K=2
Model C: K=3
```

That changed the rank order and broke the hash.

The fix:

```text
0 = not dominant
3 = dominant
```

So the system asks only:

```text
Is this variable structurally dominant, yes or no?
```

Confidence can still be scalar, but it must not alter the canonical address.

Final rule:

```text
Binary score determines address.
Confidence score determines review priority.
```

## 3. Confidence is not classification

Separate:

```text
orientation = 0 or 3
confidence = 0.00-1.00
```

Example:

```text
G=3, confidence .92
C=0, confidence .61
```

This lets different models disagree in confidence without drifting the address.

Use:

```text
0/3 = address
0.00-1.00 = confidence
Hamming distance = model agreement
review flag = uncertainty handling
```

## 4. Use Hamming distance for model agreement

When multiple AIs classify the same artifact, compare their binary vectors.

```text
Distance 0 = exact match
Distance 1 = strong match, review one variable
Distance 2 = partial match, adjudicate
Distance 3+ = unstable classification or bad prompt/input
```

This gives a measurable way to say:

```text
The models understood the same thing.
```

or:

```text
The artifact/prompt is ambiguous.
```

## 5. Fixed tie-break order prevents hash drift

When several variables are dominant, the top pair is often determined by tie-break order.

That is not an error.

Locked order:

```text
E -> C -> G -> K -> M -> T -> R -> F -> S -> Q
```

This means dense documents can have many `3`s, but the hash still forms deterministically.

Important rule:

```text
Pair 1 is an anchor, not the whole meaning.
Semantic density is preserved in the full vector and full hash.
```

## 6. C is not a quality bonus

This was one of the biggest edge corrections.

Bad version:

```text
This document is well-written, so C=3.
This checklist is coherent, so C=3.
This clock works, so C=3.
```

Correct version:

```text
C=3 only when synthesis, integration, reconciliation, or unification is the artifact's explicit dominant function.
```

A checklist may be coherent, but its function is procedure. A clock may be coherent, but its function is timekeeping. The Master Equation architecture gets `C=3` because integration is the point.

## 7. E is artifact disorder, not dark subject matter

Bad version:

```text
The document discusses disorder, so E=3.
```

Correct version:

```text
E=3 only if the artifact itself is structurally noisy, fragmented, contradictory, corrupted, redacted, illegible, or unstable.
```

A clean paper about entropy can be `E=0`. A redacted FBI document can be `E=3`. A damaged diary page can be `E=3`.

## 8. The semantic address is not the grade

The address identifies the artifact:

```text
D/N/V/A/U/R :: VECTOR :: HASH
```

The grade audits the artifact:

```text
Academic Readiness
Framework Coherence
Public Communication
Risk
```

Do not put grades into the permanent file name, because grades change after repair.

Correct relationship:

```text
Address = identity/classification
Snapshot = reconstruction
Grade = audit metadata
Ledger = explanation of the grade
```

## 9. The grade must come from score events, not vibes

The snapshot becomes grading only when every module creates score events.

A module is not grading when it says:

```text
This paper has evidence.
```

It becomes grading when it says:

```text
+2 primary source named
+2 tested thing clear
-2 evidence bridge missing
-1 counterevidence absent
```

Every score needs:

```text
metric
points
reason
evidence_quote
section
fix_to_improve
```

This is the difference between a summary and an audit.

## 10. Do not collapse the four scores

Never collapse these into one "truth score":

```text
Academic Readiness
Framework Coherence
Public Communication
Risk
```

They answer different questions.

A paper can be:

```text
Framework Coherence: A
Academic Readiness: C
Public Communication: B
Risk: High
```

That is not contradiction. That is useful.

## 11. Risk is not a semantic variable

Risk belongs to the filing/audit layer, not the semantic vector.

```text
R in semantic vector = Relation/Bond
R in filing layer = Risk
```

This requires namespacing in code and UI.

Better internal names:

```text
R_sem = Relation/Bond
R_file = Risk
```

## 12. Grades should create repair queues

A bad grade is not the end.

It should produce:

```text
repair_item
fix_to_improve
priority
affected_claims
affected_downstream_papers
```

The system's purpose is not just judgment. It is repair.

## 13. Obsidian is not the audit database

Use the split:

```text
Obsidian = human surface
Postgres = audit memory
Python/NLP = extraction/classification
LLM = reconstruction/review
HTML = review surface
Repair queue = quality-control layer
```

Do not write all audit state back into the vault as if the vault is the database. That creates drift.

The vault stores readable knowledge. Postgres stores IDs, hashes, snapshots, runs, ledgers, and repairs.

## 14. The unit is the claim, not the paper

At vault scale, the right unit is not:

```text
paper
```

but:

```text
claim_block
equation_block
evidence_block
audit_snapshot
repair_item
```

This is what makes thousands of papers possible. A document becomes a container. The machine works on structured claim units.

## 15. Every object needs stable identity

For scale, the system needs:

```text
vault_id
doc_id
note_version
content_hash
block_id
claim_id
equation_id
evidence_id
run_id
audit_snapshot_id
repair_item_id
```

Without this, you get duplicate fog.

## 16. Snapshots should append, not overwrite

Every run creates a new audit snapshot.

Do not overwrite previous audit state.

Reason:

```text
You need provenance.
You need diff history.
You need to know whether a repair improved the paper.
```

## 17. Prompt versions are schema versions

A prompt change is not "just wording." It changes extraction behavior.

So:

```text
prompt_version
schema_version
model_version
run_id
content_hash
```

all matter.

Otherwise, if classifications change later, you will not know whether the paper changed, the model changed, or the prompt changed.

## 18. NLP does first-pass classification; LLM does reconstruction

Separate the stack:

```text
Rules/Python = parsing, IDs, hashes, deterministic scoring
NLP/BERT/SBERT = block labels, embeddings, similarity, clustering
LLM = buried claims, evidence bridges, hostile review, repair reasoning
Postgres = state/provenance
HTML = review surface
```

Do not ask BERT to "understand the whole framework."

Use NLP to classify blocks and find similarity. Use LLMs to reconstruct meaning from the structured blocks.

## 19. Embeddings find neighbors; addresses classify artifacts

Embeddings are not enough.

They find semantic similarity.

The address gives structural identity.

Together:

```text
embedding = nearby meaning
Nabla address = artifact type/function
snapshot = reconstructable structure
grade = defensibility status
```

This enables queries like:

```text
Find papers similar to Grace as external input.
Find equations similar to the Master Equation.
Find claims using entropy across physics and theology.
Find papers with same structural address but different domain.
```

## 20. Affective state is a different layer

The same variables can help classify person-state, but with different rules.

Document classification:

```text
binary 0/3 for stability
```

Affective/relational-state classification:

```text
scalar 0-3 or 0-5 for sensitivity
```

Document system asks:

```text
What kind of artifact is this?
```

Affective system asks:

```text
What kind of relational/emotional posture is present right now?
```

Do not mix those scoring modes.

## 21. "Lossless" means reconstruction seed, not magic compression

Lossless does not mean every word is preserved. It means the future AI can reconstruct:

```text
thesis
claims
definitions
decisions
rationale
entities
mechanisms
open threads
proof boundaries
repair path
```

Common words can be dropped only if they are not load-bearing.

Do not delete:

```text
not
because
unless
if
then
only
before
after
therefore
however
must
may
never
```

Those carry logic.

## 22. The compression must tell the AI what not to claim

A good artifact does not only preserve what is known.

It also preserves boundaries:

```text
FORMAL
STRUCTURAL
EMPIRICAL
INTERPRETIVE
SPECULATIVE
PUBLIC-FACING
```

This prevents a future AI from turning a structural insight into an empirical proof.

## 23. Formal proof and interpretation must stay separated

For Theophysics especially:

```text
Lean proof = formal/product behavior
Structural support = architecture holds together
Interpretation = theological/metaphysical mapping
Empirical validation = external testing
```

Do not let a proof in one layer automatically certify another layer.

## 24. χ is not a factor

This was critical in the Master Equation work.

Correct:

```text
C is the tenth factor.
χ is the product/output/integrated field.
```

Incorrect:

```text
χ becomes the tenth factor.
```

That would be circular.

## 25. Raw entropy cannot positively multiply coherence

Old issue:

```text
χ = G·M·E·S·T·K·R·Q·F·C
```

If `S` means raw entropy production, higher disorder would raise coherence.

Corrected:

```text
S_prod = raw entropy production
S_eff = exp(-η S_prod)
χ = G·M_eff·E·S_eff·T·K·R·Q·F·C
```

Entropy enters as attenuation, not boost.

## 26. Raw M must become M_eff

Raw alignment:

```text
M_raw in [-1,1]
```

causes sign problems. Negative M can make χ negative and break monotonicity.

Corrected:

```text
M_eff = (1 + M_raw)/2
```

Now:

```text
opposed -> 0
neutral -> 1/2
aligned -> 1
```

That matched both the math and the reception logic.

## 27. Version A is diagnostic; Version B is canonical-ready

For the Master Equation product test:

```text
Version A = raw M, S_eff
Version B = M_eff, S_eff
```

Version A showed what fails. Version B is cleaner and should be canonical for the product kernel.

## 28. Teaching-law layers may change; formal factors should not

Separate:

```text
teaching laws / chapter organization
formal factors
spiritual interpretations
```

A law chapter can consolidate or move. But Definition 10's ten formal factors remain the anchor unless formally replaced.

## 29. Do not force a tenth teaching chapter if the factor layer already has ten

If teaching laws collapse from ten to nine, that does not automatically break the Master Equation.

Correct:

```text
10 formal factors
9 or 10 teaching movements
χ as output
```

Do not fill an empty teaching slot just to preserve symmetry.

## 30. The system should be user-controlled, not surveillance-coded

Universal semantic addressing can sound dystopian if framed badly.

Bad frame:

```text
Every file in the world becomes legible to every machine.
```

Good frame:

```text
User-controlled semantic addressing for private and institutional knowledge systems.
```

Principle:

```text
Semantic addresses are for user-controlled understanding, not involuntary exposure.
```

## Short Canonical Summary

```text
The core system stabilizes classification by scoring what the artifact is, not what it talks about; using binary 0/3 orientation rather than scalar magnitude; separating confidence from address; enforcing fixed tie-breaks; treating C as explicit synthesis only; treating E as artifact disorder only; attaching grades as audit metadata rather than names; and storing every claim, score, repair, and run as versioned structured data.

The result is not just file naming. It is a reproducible semantic operating layer for documents, claims, equations, evidence, grading, reconstruction, similarity search, and repair.
```
