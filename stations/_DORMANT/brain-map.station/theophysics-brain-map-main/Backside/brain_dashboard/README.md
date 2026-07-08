# Brain Dashboard

Read-only PySide6 dashboard that visualizes runtime state for the intake engine at a 100-foot view.

## MVP features
- Overview tab with per-NLP status cards and recent errors.
- NLP detail tab with README preview, run history, and folder summaries.
- Pipeline state tab with route-level queue/output visibility.
- Schedule tab that reads Windows Task Scheduler (Theophysics_*/FAP_* tasks).
- Logs tab with tail view over `_LOGS` files.

## Run
```bash
pip install -e .
brain-dashboard
```

## Optional smoke mode
```bash
brain-dashboard --headless-smoke-test
```

## Data contract
The dashboard reads `intake_engine/state.json` and does not mutate state.
