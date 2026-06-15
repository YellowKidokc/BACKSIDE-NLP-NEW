# FAP Pipeline Builder Prompt

Build the first executable FAP pipeline from the existing lanes.

Target manufacturing line:

```text
INTAKE
-> CLASSIFY
-> MEDIA ROUTE
-> LOSSLESS
-> VECTORIZE
-> GRADE
-> AXIOM MAP
-> OUTPUT / AI PORTAL PACKAGE
```

For each station define:

- input folder
- output folder
- review folder
- rejected folder
- manifest fields
- pass condition
- review condition
- fail condition
- next route
- Postgres table/event needed

Do not invent model calls yet. Start with deterministic file movement and manifests.
