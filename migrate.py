#!/usr/bin/env python3
"""
Migration script: JSON → SQLite
Migrates data from v0.3.0 (JSON files) to v1.0 (SQLite)
"""

import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Paths
OLD_QUEUE_FILE = Path("/tmp/a11y_queue.json")
OLD_RESULTS_FILE = Path("/tmp/a11y_results.json")
NEW_DB_FILE = Path("/home/butenhome/aiwork/data.db")
SCHEMA_FILE = Path("/home/butenhome/aiwork/schema.sql")


def generate_id(prefix: str = "") -> str:
    """Generate UUID"""
    return f"{prefix}_{uuid.uuid4().hex[:12]}" if prefix else uuid.uuid4().hex


def now_iso() -> str:
    """Current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"


def rating_to_severity(rating: str) -> str:
    """Convert old rating to severity"""
    mapping = {
        "good": "minor",
        "issues": "moderate",
        "critical": "critical",
        "skipped": "minor"
    }
    return mapping.get(rating, "moderate")


def load_json_file(path: Path) -> Optional[Dict]:
    """Load JSON file safely"""
    if not path.exists():
        print(f"⚠️  File not found: {path}")
        return None
    
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        return None


def create_database(db_path: Path, schema_path: Path):
    """Create database with schema"""
    print(f"📊 Creating database: {db_path}")
    
    # Read schema
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Create database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema
    cursor.executescript(schema)
    conn.commit()
    
    print("✅ Database created")
    return conn


def migrate_results(conn: sqlite3.Connection, results: Dict):
    """Migrate old results to new structure"""
    cursor = conn.cursor()
    
    migrated_count = 0
    
    for job_id, result in results.items():
        try:
            # Create project
            project_id = generate_id("proj")
            project_name = f"Legacy: {result.get('url', 'Unknown')[:50]}"
            
            cursor.execute("""
                INSERT INTO projects (id, name, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                project_id,
                project_name,
                'completed',
                result.get('completed_at', now_iso()),
                result.get('completed_at', now_iso())
            ))
            
            # Create target
            target_id = generate_id("target")
            cursor.execute("""
                INSERT INTO targets (id, project_id, name, url, flow_type, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                target_id,
                project_id,
                "Legacy Page",
                result.get('url', 'https://example.com'),
                'page',
                result.get('completed_at', now_iso()),
                result.get('completed_at', now_iso())
            ))
            
            # Create issue (if not "good" or "skipped")
            rating = result.get('rating', 'issues')
            if rating not in ['good', 'skipped']:
                issue_id = generate_id("issue")
                
                title = result.get('description', 'Legacy issue')
                if len(title) > 100:
                    title = title[:97] + "..."
                
                cursor.execute("""
                    INSERT INTO issues (
                        id, project_id, target_id, title, raw_note, description,
                        severity, affected_element, wcag_criterion,
                        source_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    issue_id,
                    project_id,
                    target_id,
                    title,
                    result.get('description'),
                    result.get('description'),
                    rating_to_severity(rating),
                    result.get('element'),
                    result.get('wcag_criterion'),
                    'imported',
                    'reported',
                    result.get('completed_at', now_iso()),
                    result.get('completed_at', now_iso())
                ))
            
            migrated_count += 1
            
        except Exception as e:
            print(f"⚠️  Error migrating {job_id}: {e}")
            continue
    
    conn.commit()
    return migrated_count


def backup_old_files():
    """Backup old JSON files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for old_file in [OLD_QUEUE_FILE, OLD_RESULTS_FILE]:
        if old_file.exists():
            backup_file = old_file.parent / f"{old_file.stem}_backup_{timestamp}{old_file.suffix}"
            print(f"💾 Backing up {old_file} → {backup_file}")
            old_file.rename(backup_file)


def main():
    """Main migration process"""
    print("🚀 Starting migration: JSON → SQLite")
    print("=" * 50)
    
    # Check if database already exists
    if NEW_DB_FILE.exists():
        response = input(f"⚠️  Database {NEW_DB_FILE} already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return
        NEW_DB_FILE.unlink()
    
    # Load old data
    print("\n📂 Loading old data...")
    results = load_json_file(OLD_RESULTS_FILE)
    
    if not results:
        print("⚠️  No results to migrate")
        results = {}
    else:
        print(f"✅ Loaded {len(results)} results")
    
    # Create database
    print("\n📊 Creating database...")
    conn = create_database(NEW_DB_FILE, SCHEMA_FILE)
    
    # Migrate data
    if results:
        print("\n🔄 Migrating data...")
        migrated = migrate_results(conn, results)
        print(f"✅ Migrated {migrated} results")
    
    # Close connection
    conn.close()
    
    # Backup old files
    print("\n💾 Backing up old files...")
    backup_old_files()
    
    print("\n" + "=" * 50)
    print("✅ Migration complete!")
    print(f"📊 New database: {NEW_DB_FILE}")
    print(f"💾 Old files backed up")
    
    # Statistics
    conn = sqlite3.connect(NEW_DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM projects")
    projects_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM issues")
    issues_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 Database statistics:")
    print(f"   Projects: {projects_count}")
    print(f"   Issues: {issues_count}")


if __name__ == "__main__":
    main()
