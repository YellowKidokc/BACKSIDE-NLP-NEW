# Axiom Candidates Station

**Purpose:** Convert refined Seven Questions JSON into axiom candidates.
**Status:** candidate station
**Last updated:** 2026-05-16

This station does not create final axioms. It surfaces load-bearing claims and packages them for review.

## Boundary

The 7QS surfaces the load-bearing claims. Axioms are what remain after denial, reversal, dependency, evidence, and kill-condition testing.

Pipeline:

```text
Question -> Claim -> Dependency -> Reversal -> Evidence -> Axiom Candidate -> Promoted Axiom
```

## Contract

Input:

```text
packet/WORKING/station-outputs/seven-questions/*_7QS_*.json
```

Output:

```text
packet/WORKING/station-outputs/axiom-candidates/*_AXIOM_CANDIDATES_*.json
packet/WORKING/station-outputs/axiom-candidates/*_AXIOM_CANDIDATES_*.md
packet/MACHINE/station-log.json
```

Run directly:

```bash
python station.py --seven-q "path/to/paper_7QS_YYYY-MM-DD.json" --output "path/to/_AXIOM_CANDIDATES"
```

## Promotion Statuses

- `promotion_ready`
- `strong_candidate`
- `candidate_needs_work`
- `weak_candidate`
- `blocked_missing_kill_conditions`

No workflow should treat these as final axioms without a review/promotion station or human review step.
