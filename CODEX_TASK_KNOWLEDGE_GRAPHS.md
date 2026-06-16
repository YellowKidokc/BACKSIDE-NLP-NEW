# CODEX TASK: Knowledge Graph Generators (1-4)
## POF 2828 | June 16, 2026

### Goal
Build 4 knowledge graph generators in `\\192.168.2.50\brain\17_KNOWLEDGE_GRAPHS\generators\`.
Each reads its input source, builds a networkx graph, exports to graph.json + graph.html (pyvis) + summary.md.

### Full architecture spec
Read `\\192.168.2.50\brain\17_KNOWLEDGE_GRAPHS\ARCHITECTURE.md` first — it has node/edge definitions for all 8 graph types. Build the first 4.

### Generator 1: TAG GRAPH
**Input:** JSON files in `17_KNOWLEDGE_GRAPHS\INPUT\` — each file has a `tags` array from classifier output
**Nodes:** Each unique tag (e.g., "grace", "entropy", "Trinity")
**Edges:** Two tags that appear in the same paper get an edge. Weight = number of papers they co-occur in.
**Output:** `OUTPUT\tag_graph\` — graph.html, graph.json, summary.md
**Node color:** By frequency (more papers = brighter)
**Node size:** By degree (more connections = bigger)

### Generator 2: AXIOM DEPENDENCY GRAPH
**Input:** `canonical_chain_nodes.psv` from paper-proof-grader.station\REFERENCE\ (pipe-delimited, columns: position, display_id, node_id, name, formal_statement, family, node_type, level, depends_on, kill_condition)
**Nodes:** Each axiom/theorem/definition (display_id as label)
**Edges:** `depends_on` column contains comma-separated node_ids that this node depends on. Create directed edges (dependency → dependent).
**Output:** `OUTPUT\axiom_graph\`
**Node color:** By level/layer (Layer 0 = foundation color, higher layers = lighter)
**Node size:** By how many other nodes depend on it (more dependents = bigger = more foundational)
**Special:** Nodes with kill_conditions get a red border. Orphan nodes (no depends_on AND nothing depends on them) get flagged in summary.md.

### Generator 3: MASTER EQUATION GRAPH
**Input:** JSON files in `17_KNOWLEDGE_GRAPHS\INPUT\` — each file has a `master_eq_vars` dict mapping variable letters (G,M,E,S,T,K,R,Q,F,C) to mention counts
**Nodes:** The 10 super-factors: G (Grace), M (Moral Alignment), E (Entropy), S (Shannon), T (Time), K (Knowledge), R (Redemptive Order), Q (Quantum Consciousness), F (Faith), C (Coherence)
**Edges:** Two variables that appear in the same paper get an edge. Weight = number of papers they co-occur in.
**Additional nodes:** Each paper as a smaller node, connected to the variables it references.
**Output:** `OUTPUT\master_eq_graph\`
**Node color:** Each variable gets a fixed canonical color (use warm palette for spiritual-primary vars, cool palette for physics-primary vars)
**Summary:** Which variable pairs are well-developed (many shared papers) vs neglected (few or no shared papers).

### Generator 4: PAPER-TO-PAPER GRAPH
**Input:** JSON files in `17_KNOWLEDGE_GRAPHS\INPUT\` — each file represents one paper with tags, claims, variables, scores
**Nodes:** Each paper (paper_id as label)
**Edges:** Papers sharing 3+ tags, or same dominant Master Equation variable, or same Law reference. Weight = number of shared elements.
**Output:** `OUTPUT\paper_graph\`
**Node color:** By series (GTQ = blue family, MDA = green family, Logos = gold family)
**Node size:** By total claim count
**Note:** An existing `graph_builder.py` at `paper-intelligence-suite.station\07_KNOWLEDGE_GRAPHS\` does something similar with networkx+pyvis. Reference it but build fresh for this input format.

### Shared Requirements
- Python 3.10+
- `pip install networkx pyvis` (already available in the station venv)
- Each generator is a standalone script: `python tag_graph.py`
- Each reads from `17_KNOWLEDGE_GRAPHS\INPUT\` and writes to its `OUTPUT\{type}_graph\` subfolder
- graph.html should be interactive (pyvis) — clickable nodes, hover for details, draggable layout
- graph.json should be the raw networkx node-link format for downstream use
- summary.md should list: total nodes, total edges, top 10 most-connected nodes, orphans, clusters (Louvain if available)

### Test
Create a sample input JSON in `INPUT\` with 3-5 fake papers, run all 4 generators, verify HTML files open in browser and show interactive graphs.

### Input JSON Schema (per paper)
```json
{
  "paper_id": "GTQ_01_Why_Time_Is_Grace",
  "series": "GTQ",
  "tags": ["grace", "entropy", "measurement", "collapse"],
  "claims": [
    {"text": "...", "classification": "THEOREM", "7q_score": 5, "axiom_hits": ["A1.1", "BC2"]}
  ],
  "master_eq_vars": {"G": 12, "E": 8, "Q": 4},
  "laws_referenced": [1, 5, 7],
  "scripture_refs": ["Genesis 3:7"],
  "fruit_score": 0.72,
  "anti_fruit_score": 0.08,
  "word_count": 5001,
  "claim_count": 30
}
```
