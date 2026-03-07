"""
Base repository with common CRUD operations
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from database import db


def generate_id(prefix: str = "") -> str:
    """Generate UUID with optional prefix"""
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}" if prefix else uid


def now_iso() -> str:
    """Current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"


def row_to_dict(row) -> Dict[str, Any]:
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return dict(row)


class BaseRepository:
    """Base repository with common operations"""
    
    table_name: str = None
    id_prefix: str = ""
    
    def create(self, data: Dict[str, Any]) -> str:
        """Create new record"""
        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = generate_id(self.id_prefix)
        
        # Add timestamps if not provided (only if table has these columns)
        if 'created_at' not in data:
            data['created_at'] = now_iso()
        if 'updated_at' not in data and self.table_name not in ['evidence', 'checklist_results']:
            data['updated_at'] = now_iso()
        
        # Add started_at for test_sessions
        if self.table_name == 'test_sessions' and 'started_at' not in data:
            data['started_at'] = now_iso()
        
        # Build INSERT query
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        
        db.execute(query, tuple(data.values()))
        return data['id']
    
    def get(self, id: str) -> Optional[Dict[str, Any]]:
        """Get record by ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        row = db.fetchone(query, (id,))
        return row_to_dict(row)
    
    def update(self, id: str, data: Dict[str, Any]) -> bool:
        """Update record"""
        # Add updated_at
        data['updated_at'] = now_iso()
        
        # Build UPDATE query
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?"
        
        cursor = db.execute(query, tuple(data.values()) + (id,))
        return cursor.rowcount > 0
    
    def delete(self, id: str) -> bool:
        """Delete record"""
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor = db.execute(query, (id,))
        return cursor.rowcount > 0
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List all records"""
        query = f"SELECT * FROM {self.table_name} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        rows = db.fetchall(query, (limit, offset))
        return [row_to_dict(row) for row in rows]
    
    def count(self) -> int:
        """Count records"""
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        row = db.fetchone(query)
        return row[0] if row else 0
