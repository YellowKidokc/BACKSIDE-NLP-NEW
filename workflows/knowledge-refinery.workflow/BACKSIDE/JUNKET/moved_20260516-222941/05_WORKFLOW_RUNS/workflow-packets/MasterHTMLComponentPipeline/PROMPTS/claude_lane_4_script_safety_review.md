# Claude Lane 4: Imported Script Safety Review

Assignment: review the 18 imported Master HTML scripts for production safety.

Inputs:

- `SCRIPTS/imported/html_master_workflow`
- `CONFIG/script_registry.json`

Return one row per script:

- script id/path
- purpose
- expected inputs
- hard-coded paths
- dry-run support
- writes in place
- backup behavior
- safe wrapper needed yes/no
- recommended GUI exposure

Rules:

- Do not run write-capable scripts against production folders.
- Static review first.
- Flag scripts that need wrappers before GUI use.
