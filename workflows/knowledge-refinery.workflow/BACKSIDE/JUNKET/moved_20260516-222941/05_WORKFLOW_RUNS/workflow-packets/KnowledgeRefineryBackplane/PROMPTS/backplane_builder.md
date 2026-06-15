# Backplane Builder Prompt

You are building the automated production backplane for Theophysics paper and
vault workflows.

Keep these boundaries:

- Keep David-facing front doors simple.
- Keep heavy models, vector indexes, databases, and vault dumps outside this repo.
- Use `CONFIG/source_registry.example.json` to find live source systems.
- Use `CONFIG/model_stations.example.json` to find model stations.
- Prefer workflow packets over one monolithic app.
- Every station must emit a manifest with input, status, confidence, evidence,
  outputs, and next routes.

Target output shape:

```text
paper/source in
-> graded outputs
-> claim rows
-> station checks
-> rigor gates
-> summary layers
-> vault page
-> AI portal package
-> archive
```

Do not claim proof because a model produced a label. Model labels are review
signals. Proof requires the linked formal, empirical, or source artifact.
