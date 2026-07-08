---
title: "Lossless Context Compression + Semantic Addressing Protocol v1.0"
domain: "TECH"
state: "W"
access: "AI_RESEARCH"
use: "T"
risk: "R1"
---

# LOSSLESS CONTEXT COMPRESSION + SEMANTIC ADDRESSING PROTOCOL v1.0

Use for document ingestion, AI-to-AI handoff, vault indexing, contradiction detection, and reconstruction.

Goal: convert any article, note, paper, transcript, or file into a dense, structured reconstruction artifact.

The system compresses the provided document into a self-contained reconstruction artifact that another advanced AI, NLP pipeline, or database system can later use to reconstruct the document's structure, meaning, claims, evidence, unresolved issues, and classification.

It does not summarize loosely, merely list topics, or omit decisions, claims, definitions, constraints, equations, evidence, disagreements, rejected alternatives, unresolved questions, or future-use seeds.

Compression goal: maximum density with maximum reconstructability.

Core rule: compress; do not delete. Common words may be removed only when they are not load-bearing. Preserve relationship words when they affect meaning: not, because, unless, except, before, after, therefore, however, if, then, only, must, may, should, never.

## Semantic Address

Assign the document a Nabla-style semantic address: D/N/V/A/U/R :: VECTOR :: HASH.

D = Domain. N = Named Entity. V = Version or State. A = Audience or Access. U = Use or Direction. R = Risk.

Lifecycle state values: Draft, Working, Final, Published, Archived, Deprecated. Risk values: R0 public low sensitivity, R1 internal research, R2 private PII sensitive, R3 legal financial formal consequence, R4 life-critical medical safety-critical.

## Ten Variable Semantic Vector

Score each variable only 0 or 3. Score the document as an artifact: what it structurally is, how it functions, and how it presents its content. Do not score based on subject matter alone.

G = Authority/Ground. M = Mechanism/Action. E = Entropy/Disorder. S = Identity/Self. T = Time/Sequence. K = Knowledge/Info. R = Relation/Bond. Q = Experience/Felt. F = Faith/Trust. C = Coherence/Unity.

E=3 only when the artifact itself contains disorder, contradiction, fragmentation, corruption, or ambiguity. C=3 only when synthesis, integration, or unification is the artifact's explicit dominant function.

Tie-break order: E, C, G, K, M, T, R, F, S, Q. Rank variables highest to lowest and pair strongest with weakest inward to construct the hash.

## Reconstruction Artifact

Return: COMPRESSION_DECLARATION, ADDRESS, SPINE, ENTITIES, SEMANTICS, CLAIM_ARCH, EVIDENCE_CHAIN, KILL_ARCH, EQ_SEM, DOMAIN_BOUNDARY, MECHANISM_GRAPH, REVIEWER_SEEDS, OVERSTATE_PATTERN, LEDGER_SCHEMA, FOUR_SCORE_DASHBOARD, CROSS_DEP, EIGHT_GAPS, SEED_BANK, OPEN_THREADS, DECOMPRESS, CHECK, RECOVERY_KEY.

Major claims require surface_claim, buried_claim, operational_claim, rhetorical_load, domain_shift, and domain_badges. Evidence-bearing claims require primary_source, secondary_source, tertiary_source, tested_thing, connection_to_claim, gap, and counterevidence_present. Equations require equation, role, status, undefined_vars, dimensional_status, derivation_present, computable, and known_theory_comparison.

The grade must not become the filename. The grade is audit metadata. The permanent identifier is D/N/V/A/U/R :: VECTOR :: HASH.

The system must support batch processing thousands of Markdown notes. Do not overwrite snapshots; append new audit runs with run_id and content_hash.

## Pipeline Build Requirement

Build a Python/NLP pipeline that implements the protocol. Use deterministic rule-based extraction where possible: Markdown headings, frontmatter, equations, citations, keyword/domain badges, overstatement words, section IDs, and content hashes.

Use NLP models where useful: sentence embeddings for similarity search, BERT/SBERT/DeBERTa classifiers for block classification, clustering for related claims, and contradiction engine for claim conflicts.

Use an LLM only for the parts NLP cannot reliably do: buried_claim, operational_claim, evidence_bridge, implicit_kill, hostile reviewer attack, and repair recommendation.

Required database objects: vault_id, doc_id, note_version, content_hash, block_id, claim_id, equation_id, evidence_id, run_id, audit_snapshot_id, repair_item_id.

Pipeline: load Markdown; parse frontmatter; split by headings and paragraphs; assign stable block IDs; classify blocks; generate embeddings; extract structured objects; assign Nabla address; compute vector and hash; generate four separate grades; write score ledger; render JSON; render HTML snapshot; store in Postgres; support reconstruction test.

Return folder structure, Python modules, Pydantic schemas, Postgres table schema, CLI commands, sample JSON output, sample HTML output, and test plan.

## AI Layer Direction

If the protocol can build a lossless model of the framework, then everything should produce a lossless model. The lossless model becomes the AI-readable layer of the website. An AI can inspect the lossless artifact first, understand where attributes should live semantically and vectorially, then open the original document only when it needs source-level proof or disproof.
