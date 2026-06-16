# Chi Tagging Workflow

**Purpose:** build the canon reference index that should drive chi-variable tagging for Postgres corpus rows.

This workflow does not write to Postgres yet. It produces the deterministic reference layer first.

## Station Chain

```text
master-equation-canon
trinity-canon
fruits-spirit-canon
operators-canon
-> canon-index.aggregate.json
```

## Run

```powershell
python Backside\workflows\chi-tagging.workflow\pipeline.py
```

Outputs:

```text
X:\EXPORTS\chi-tagging\<run_id>\
X:\Backside\_state\chi-tagging\<run_id>\
```

## Database Targets After Index Build

1. `public.cross_domain` -> add/populate `chi_vars text[]`
2. `framework_topology.canonical_axioms` -> add/populate `chi_vars text[]`
3. `framework_math.equation_terms` -> link remaining equations to variable terms

## Granularity Rule

```text
word/phrase = trigger
sentence = evidence span
paragraph/block = chi_vars assignment
row/document = aggregate
```

