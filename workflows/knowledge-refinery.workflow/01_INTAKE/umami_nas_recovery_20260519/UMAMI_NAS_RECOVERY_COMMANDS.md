# Umami NAS Recovery Commands

**Date:** 2026-05-19  
**Goal:** Pause/recover self-hosted Umami on Synology Docker/Container Manager without deleting analytics data.

## Safety Rules

- Do not delete containers.
- Do not delete images.
- Do not delete projects.
- Do not delete volumes.
- Do not run `docker compose down -v`.
- Stop only the Umami app/web container if pausing analytics.
- Keep the Postgres/database container and volume intact.

## If Docker / Container Manager Is Off

Umami is already offline. Tracking requests may fail, but the database should be safe.

For password recovery, temporarily start Synology **Container Manager** again, reset the password, then stop only the Umami web/app container if you still want analytics paused.

## SSH In

From Windows PowerShell:

```powershell
ssh Yellowkid@192.168.1.177
```

If that host is not the active NAS, try:

```powershell
ssh Yellowkid@dlowenas
```

## Inspect Only

Run these first:

```bash
hostname
whoami
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker compose ls
```

Find likely Umami files:

```bash
find /volume1/docker -maxdepth 5 \( -iname '*umami*' -o -name 'docker-compose.yml' -o -name 'compose.yaml' \) 2>/dev/null
```

## Pause Umami Safely

Find the app container:

```bash
docker ps -a --format '{{.Names}} {{.Image}} {{.Status}}' | grep -i umami
```

Stop only the web/app container, not the database:

```bash
docker stop <umami_app_container_name>
```

If using compose and the service is named `umami`:

```bash
docker compose stop umami
```

## Password Reset Path

First try the default login after the app is running:

```text
username: admin
password: umami
```

If that fails, inspect the app container environment:

```bash
docker inspect <umami_app_container_name> --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -E 'DATABASE_URL|POSTGRES|UMAMI'
```

Find the database container:

```bash
docker ps -a --format '{{.Names}} {{.Image}} {{.Status}}' | grep -Ei 'postgres|db|umami'
```

Open psql. The username/database may be `umami`, `postgres`, or whatever appears in `DATABASE_URL`.

Common path:

```bash
docker exec -it <postgres_container_name> psql -U umami -d umami
```

Inside psql, inspect tables:

```sql
\dt
select username, role from "user";
```

Reset admin to the default Umami password `umami`:

```sql
UPDATE "user"
SET password = '$2b$10$BUli0c.muyCW1ErNJc3jL.vFRFtFJWrT8/GcR4A.sUdCznaXiqFXa'
WHERE username = 'admin';
```

Then:

```sql
\q
```

Restart the Umami app container:

```bash
docker restart <umami_app_container_name>
```

Log in with:

```text
admin / umami
```

Immediately change the password in Umami.

## If the Table Is Not `"user"`

Do not guess. Run:

```sql
\dt
```

Then inspect likely tables:

```sql
select * from "user" limit 1;
select * from "account" limit 1;
```

Stop and ask Codex before updating anything else.

## Tracking Script Pause

If the site still has the Umami tracker in the HTML header, remove or comment it later:

```html
<script defer src="https://.../script.js" data-website-id="..."></script>
```

That pauses collection without touching Docker or database data.

## 2026-05-19 Recovery Result

- SSH key access was established temporarily and then removed from NAS
  `authorized_keys`.
- Synology Docker socket was temporarily changed to group `administrators` so
  the admin user could inspect containers without logging the NAS password in
  shell commands.
- Containers found:
  - `Umami` — `ghcr.io/umami-software/umami:latest`
  - `Umami-DB` — `postgres:15-alpine`
- Database confirmed:
  - database: `umami`
  - user: `umamiuser`
  - schema includes `"user"` table.
- Admin password reset succeeded with `UPDATE 1`.
- `Umami-DB` is running healthy.
- `Umami` is running healthy on NAS port `3999`.
- HTTP check from Windows returned status `200`.
- Container-local heartbeat returned `{"ok":true}`.

Current login:

```text
URL: http://192.168.1.177:3999
username: admin
password: umami
```

Change the password immediately after login.

Optional cleanup after everything is confirmed:

```powershell
ssh -tt Yellowkid@192.168.1.177 "sudo chgrp root /var/run/docker.sock && sudo chmod 660 /var/run/docker.sock && ls -l /var/run/docker.sock"
```
