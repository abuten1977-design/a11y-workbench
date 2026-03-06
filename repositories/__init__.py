"""
Base repository with common CRUD operations
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from database import get_db


def generate_id(prefix: str = "") -> str:
    """Generate UUID with optional prefix"""
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}" if prefix else uid


def now_iso() -> str:
    """Current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"


def row_to_dict(row) -> Dict:
    """Convert sqlite3.Row to dict"""
    return dict(row) if row else None


def rows_to_list(rows) -> List[Dict]:
    """Convert list of sqlite3.Row to list of dicts"""
    return [dict(row) for row in rows]
