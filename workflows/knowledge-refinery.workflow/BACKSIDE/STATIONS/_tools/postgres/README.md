# Postgres (canonical source of truth)

Backside assumption:
- Postgres is canonical for IDs + text + metadata.
- Vector indexes are disposable mirrors (rebuildable from Postgres).

Connection (from your notes):
- host: `192.168.1.177`
- port: `2665`

Put credentials/DB name into:
- `postgres.env.example` (copy to `postgres.env` locally; do not commit secrets)

