"""
Database connection and utilities
"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# Database path
DB_PATH = Path(__file__).parent / "data.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


@contextmanager
def get_db():
    """Context manager for database connection"""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(schema_path: Optional[Path] = None):
    """Initialize database with schema"""
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"
    
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    with get_db() as conn:
        conn.executescript(schema)
