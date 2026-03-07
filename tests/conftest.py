"""Pytest configuration and fixtures"""
import pytest
import sqlite3
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture(autouse=True, scope="function")
def setup_test_db():
    """Setup test database before each test"""
    from database import db
    
    # Use test database file
    test_db_path = Path(__file__).parent / "test.db"
    
    # Remove if exists
    if test_db_path.exists():
        test_db_path.unlink()
    
    # Save original
    original_path = db.db_path
    original_conn = db._conn
    
    # Set test database
    db.db_path = test_db_path
    db._conn = None
    
    # Create schema
    schema_path = Path(__file__).parent.parent / "schema.sql"
    with open(schema_path) as f:
        schema = f.read()
    
    conn = db.connect()
    conn.executescript(schema)
    conn.commit()
    
    yield
    
    # Cleanup
    db.close()
    if test_db_path.exists():
        test_db_path.unlink()
    
    # Restore
    db.db_path = original_path
    db._conn = original_conn
