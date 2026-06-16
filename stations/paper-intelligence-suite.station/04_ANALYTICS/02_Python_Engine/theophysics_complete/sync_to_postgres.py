#!/usr/bin/env python3
"""
Sync Breakthrough Vault (SQLite) → PostgreSQL
Mirrors local coherence.db to Postgres for team access
"""

import sqlite3
import psycopg2
from psycopg2.extras import execute_batch
import sys
from datetime import datetime

# ============================================
# Configuration
# ============================================
SQLITE_DB = "coherence.db"  # Your local Breakthrough Vault
POSTGRES_CONFIG = {
    'host': 'localhost',
    'database': 'theophysics',
    'user': 'postgres',
    'password': 'postgres'
}

# ============================================
# Main Sync Function
# ============================================
def sync_breakthrough_to_postgres():
    """
    Sync all tables from SQLite → PostgreSQL
    """
    print("=" * 80)
    print("BREAKTHROUGH VAULT → POSTGRESQL SYNC")
    print("=" * 80)
    
    # Connect to both databases
    try:
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cur = sqlite_conn.cursor()
        
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        pg_cur = pg_conn.cursor()
        
        print(f"\n✓ Connected to SQLite: {SQLITE_DB}")
        print(f"✓ Connected to PostgreSQL: {POSTGRES_CONFIG['database']}")
        
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        return False
    
    # Sync each table
    tables_to_sync = [
        ('notes', sync_notes),
        ('concepts', sync_concepts),
        ('co_mentions', sync_co_mentions),
        ('edges', sync_edges),
        ('metrics', sync_metrics),
        ('duplicates', sync_duplicates)
    ]
    
    for table_name, sync_func in tables_to_sync:
        print(f"\n📊 Syncing {table_name}...")
        try:
            count = sync_func(sqlite_cur, pg_cur, pg_conn)
            print(f"   ✓ Synced {count} rows")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            pg_conn.rollback()
            continue
    
    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    
    print("\n" + "=" * 80)
    print("✓ SYNC COMPLETE")
    print("=" * 80)
    
    return True

# ============================================
# Table-Specific Sync Functions
# ============================================

def sync_notes(sqlite_cur, pg_cur, pg_conn):
    """Sync notes table"""
    sqlite_cur.execute("SELECT * FROM notes")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    # Clear existing data in Postgres
    pg_cur.execute("TRUNCATE breakthrough.notes CASCADE")
    
    # Prepare insert statement
    insert_sql = """
        INSERT INTO breakthrough.notes 
        (uid, title, path, domain, tags, word_count, hash, updated_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET
            title = EXCLUDED.title,
            path = EXCLUDED.path,
            domain = EXCLUDED.domain,
            tags = EXCLUDED.tags,
            word_count = EXCLUDED.word_count,
            hash = EXCLUDED.hash,
            updated_at = EXCLUDED.updated_at
    """
    
    # Convert rows to proper format
    data = []
    for row in rows:
        # Convert tags from comma-separated to array
        tags = row['tags'].split(',') if row['tags'] else []
        data.append((
            row['uid'],
            row['title'],
            row['path'],
            row['domain'],
            tags,  # PostgreSQL array
            row['word_count'],
            row['hash'],
            row['updated_at'],
            row['created_at']
        ))
    
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

def sync_concepts(sqlite_cur, pg_cur, pg_conn):
    """Sync concepts table"""
    sqlite_cur.execute("SELECT * FROM concepts")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    pg_cur.execute("TRUNCATE breakthrough.concepts CASCADE")
    
    insert_sql = """
        INSERT INTO breakthrough.concepts (concept, mentions)
        VALUES (%s, %s)
        ON CONFLICT (concept) DO UPDATE SET
            mentions = EXCLUDED.mentions
    """
    
    data = [(row['concept'], row['mentions']) for row in rows]
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

def sync_co_mentions(sqlite_cur, pg_cur, pg_conn):
    """Sync co_mentions table"""
    sqlite_cur.execute("SELECT * FROM co_mentions")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    pg_cur.execute("TRUNCATE breakthrough.co_mentions")
    
    insert_sql = """
        INSERT INTO breakthrough.co_mentions (concept1, concept2, count)
        VALUES (%s, %s, %s)
        ON CONFLICT (concept1, concept2) DO UPDATE SET
            count = EXCLUDED.count
    """
    
    data = [(row['concept1'], row['concept2'], row['count']) for row in rows]
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

def sync_edges(sqlite_cur, pg_cur, pg_conn):
    """Sync edges table"""
    sqlite_cur.execute("SELECT * FROM edges")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    pg_cur.execute("TRUNCATE breakthrough.edges")
    
    insert_sql = """
        INSERT INTO breakthrough.edges (src, dst, rel, weight, created_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (src, dst, rel) DO UPDATE SET
            weight = EXCLUDED.weight,
            created_at = EXCLUDED.created_at
    """
    
    data = [(
        row['src'], 
        row['dst'], 
        row['rel'], 
        row['weight'], 
        row.get('created_at', datetime.now())
    ) for row in rows]
    
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

def sync_metrics(sqlite_cur, pg_cur, pg_conn):
    """Sync metrics table"""
    sqlite_cur.execute("SELECT * FROM metrics")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    pg_cur.execute("TRUNCATE breakthrough.metrics")
    
    insert_sql = """
        INSERT INTO breakthrough.metrics (uid, sis, lcs, sri, computed_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET
            sis = EXCLUDED.sis,
            lcs = EXCLUDED.lcs,
            sri = EXCLUDED.sri,
            computed_at = EXCLUDED.computed_at
    """
    
    data = [(
        row['uid'],
        row['sis'],
        row['lcs'],
        row['sri'],
        row.get('computed_at', datetime.now())
    ) for row in rows]
    
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

def sync_duplicates(sqlite_cur, pg_cur, pg_conn):
    """Sync duplicates table"""
    sqlite_cur.execute("SELECT * FROM duplicates")
    rows = sqlite_cur.fetchall()
    
    if not rows:
        return 0
    
    pg_cur.execute("TRUNCATE breakthrough.duplicates")
    
    insert_sql = """
        INSERT INTO breakthrough.duplicates 
        (uid1, uid2, similarity, exact, detected_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (uid1, uid2) DO UPDATE SET
            similarity = EXCLUDED.similarity,
            exact = EXCLUDED.exact,
            detected_at = EXCLUDED.detected_at
    """
    
    data = [(
        row['uid1'],
        row['uid2'],
        row['similarity'],
        row.get('exact', False),
        row.get('detected_at', datetime.now())
    ) for row in rows]
    
    execute_batch(pg_cur, insert_sql, data)
    pg_conn.commit()
    
    return len(rows)

# ============================================
# Verification Queries
# ============================================

def verify_sync(pg_config):
    """
    Verify the sync was successful
    """
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    conn = psycopg2.connect(**pg_config)
    cur = conn.cursor()
    
    tables = ['notes', 'concepts', 'co_mentions', 'edges', 'metrics', 'duplicates']
    
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM breakthrough.{table}")
        count = cur.fetchone()[0]
        print(f"\n✓ breakthrough.{table}: {count:,} rows")
    
    # Show some sample data
    print("\n" + "=" * 80)
    print("SAMPLE DATA")
    print("=" * 80)
    
    cur.execute("""
        SELECT concept, mentions 
        FROM breakthrough.concepts 
        ORDER BY mentions DESC 
        LIMIT 10
    """)
    print("\nTop 10 concepts:")
    for row in cur.fetchall():
        print(f"  {row[0]:30} | {row[1]} mentions")
    
    conn.close()

# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    print("\n🔄 Starting Breakthrough Vault sync...")
    print(f"SQLite source: {SQLITE_DB}")
    print(f"PostgreSQL target: {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['database']}")
    print()
    
    if sync_breakthrough_to_postgres():
        verify_sync(POSTGRES_CONFIG)
        print("\n✓ All done!\n")
    else:
        print("\n❌ Sync failed\n")
        sys.exit(1)
