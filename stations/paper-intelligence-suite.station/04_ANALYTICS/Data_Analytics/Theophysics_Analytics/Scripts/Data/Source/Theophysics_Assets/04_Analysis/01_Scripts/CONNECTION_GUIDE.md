# Connection Guide - Cloudflare & PostgreSQL

## Quick Start

Run the setup script:
```bash
python connection_setup.py
```

This will guide you through setting up both Cloudflare and PostgreSQL connections.

---

## Cloudflare Setup

### 1. Get API Token

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Edit Cloudflare Workers" template
4. Add permissions:
   - Workers: Edit
   - R2: Read & Write
   - Pages: Edit
   - D1: Edit
5. Copy the token

### 2. Get Account ID

1. Go to: https://dash.cloudflare.com/
2. Find your Account ID in the right sidebar
3. Copy it

### 3. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:CLOUDFLARE_API_TOKEN="your-token-here"
$env:CLOUDFLARE_ACCOUNT_ID="your-account-id-here"
```

**Linux/Mac:**
```bash
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="your-account-id-here"
```

### 4. Test Connection

```python
from cloudflare_connector import CloudflareConnector

connector = CloudflareConnector()
if connector.test_connection():
    print("✅ Connected!")
```

---

## PostgreSQL Setup

### 1. Install PostgreSQL

**Windows:**
- Download: https://www.postgresql.org/download/windows/
- Use installer (includes pgAdmin)

**Linux:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

**Mac:**
```bash
brew install postgresql
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE theophysics_research;

# Exit
\q
```

### 3. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_DB="theophysics_research"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="your-password"
```

**Linux/Mac:**
```bash
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="theophysics_research"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="your-password"
```

### 4. Test Connection

```python
from postgres_connector import PostgresConnector

connector = PostgresConnector()
if connector.test_connection():
    print("✅ Connected!")
```

---

## Using in Your Code

### Cloudflare Example

```python
from cloudflare_connector import CloudflareConnector

# Initialize
connector = CloudflareConnector()

# List Workers
workers = connector.list_workers()
print(f"Found {len(workers)} workers")

# List R2 buckets
buckets = connector.list_r2_buckets()
print(f"Found {len(buckets)} buckets")

# Create R2 bucket
result = connector.create_r2_bucket("my-images")
print(f"Created: {result}")
```

### PostgreSQL Example

```python
from postgres_connector import PostgresConnector

# Initialize
connector = PostgresConnector()

# Execute query
results = connector.execute_query(
    "SELECT * FROM definitions WHERE phrase = %s",
    ("Logos",)
)

# Execute command
success = connector.execute_command(
    "INSERT INTO definitions (phrase, definition) VALUES (%s, %s)",
    ("Test", "A test definition")
)

# Get table info
columns = connector.get_table_info("definitions")
for col in columns:
    print(f"{col['column_name']}: {col['data_type']}")
```

---

## Integration with AI-Swarm

### Cloudflare Workers

Your AI-Swarm is already deployed to Cloudflare Workers. The connector can:
- List deployed workers
- Deploy new versions
- Monitor usage

### R2 for Images

Store images in R2, then reference in AI-Swarm tasks:
```python
# Upload image to R2 (use wrangler or boto3)
# Then use URL in AI-Swarm task
task = {
    "type": "image_classification",
    "prompt": f"Classify image at https://r2.yourdomain.com/images/uuid.png"
}
```

### Postgres for Results

Store AI-Swarm results in Postgres:
```python
# After AI-Swarm processes image
result = ai_swarm.get_task_result(task_id)

# Save to Postgres
connector.execute_command(
    "INSERT INTO image_classifications (uuid, metadata, explanation) VALUES (%s, %s, %s)",
    (image_uuid, result["metadata"], result["explanation"])
)
```

---

## Troubleshooting

### Cloudflare

**"API token invalid"**
- Check token has correct permissions
- Regenerate token if needed

**"Account ID not found"**
- Verify account ID in dashboard
- Check you're using the right account

### PostgreSQL

**"Connection refused"**
- Is PostgreSQL running? (`pg_isready`)
- Check firewall settings
- Verify host/port

**"Authentication failed"**
- Check username/password
- Verify pg_hba.conf allows connections
- Try `psql -U postgres` to test

**"Database does not exist"**
- Create database: `createdb theophysics_research`
- Or use existing database name

---

## Security Notes

1. **Never commit API tokens or passwords to Git**
2. **Use environment variables** for sensitive data
3. **Config files** are saved to `~/.cloudflare/` and `~/.postgres/` (passwords excluded)
4. **Use `.env` files** for local development (add to `.gitignore`)

---

## Next Steps

1. ✅ Run `connection_setup.py` to configure
2. ✅ Test connections
3. ✅ Integrate with AI-Swarm
4. ✅ Start processing images!

