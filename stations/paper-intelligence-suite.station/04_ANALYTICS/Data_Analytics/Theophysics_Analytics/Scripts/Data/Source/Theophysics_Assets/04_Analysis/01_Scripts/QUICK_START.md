# Quick Start - Connection Setup

## Step 1: Install Requirements

**Double-click:** `INSTALL_CONNECTIONS.bat`

This will:
- Check Python installation
- Install `requests` library (for Cloudflare)
- Install `psycopg2-binary` (for PostgreSQL)

---

## Step 2: Configure Connections

**Double-click:** `SETUP_CONNECTIONS.bat`

This will launch an interactive setup that asks for:

### Cloudflare
- API Token (get from https://dash.cloudflare.com/profile/api-tokens)
- Account ID (get from https://dash.cloudflare.com/ - right sidebar)

### PostgreSQL
- Host (default: localhost)
- Port (default: 5432)
- Database (default: theophysics_research)
- User (default: postgres)
- Password

---

## Step 3: Test Connections

**Double-click:** `TEST_CONNECTIONS.bat`

This will test both connections and show status.

---

## Troubleshooting

### "Python is not installed"
- Install Python 3.8+ from https://www.python.org/
- Make sure "Add to PATH" is checked during installation

### "Module not found"
- Run `INSTALL_CONNECTIONS.bat` again
- Or manually: `pip install requests psycopg2-binary`

### Cloudflare connection failed
- Check API token has correct permissions
- Check account ID is correct
- Token should have: Workers, R2, Pages permissions

### PostgreSQL connection failed
- Is PostgreSQL installed? https://www.postgresql.org/download/
- Is it running? Check services or run `pg_isready`
- Is the database created? Run `createdb theophysics_research`
- Are credentials correct?

---

## What's Next?

Once connected:
- Use Cloudflare for AI-Swarm image processing
- Store images in R2
- Deploy papers to Cloudflare Pages
- Store results in PostgreSQL
- Integrate everything!

