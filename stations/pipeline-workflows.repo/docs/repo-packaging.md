# Repo Packaging Rules

Put these in Git:

- station code
- Python scripts
- batch and PowerShell launchers
- prompt files
- schemas and migrations
- config examples
- README files
- small test fixtures
- packet templates

Keep these local:

- `pipeline.config.json`
- packet `INPUT/`, `OUTPUT/`, `REVIEW/`, `ARCHIVE/`, `ERROR/`, and `LOGS/`
- `STATUS.json` and `MANIFEST.json`
- model weights
- embeddings
- vector databases
- raw private vault dumps
- runtime databases
- API keys and tokens
- large generated outputs

Git CLI can push many files. The practical limits are privacy and file size, not file count.
