"""
Database connection management
"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

# Default database path
DEFAULT_DB_PATH = Path(__file__).parent / "data.db"


class Database:
    """Database connection manager"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self._conn: Optional[sqlite3.Connection] = None
    
    def connect(self) -> sqlite3.Connection:
        """Get or create connection"""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row  # Access columns by name
        return self._conn
    
    def close(self):
        """Close connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
    
    @contextmanager
    def transaction(self):
        """Transaction context manager"""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def execute(self, query: str, params: tuple = ()):
        """Execute query"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def fetchone(self, query: str, params: tuple = ()):
        """Fetch one row"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
    def fetchall(self, query: str, params: tuple = ()):
        """Fetch all rows"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


# Global database instance
db = Database()
