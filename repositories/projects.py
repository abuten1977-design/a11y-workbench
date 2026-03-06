"""
Projects repository
"""
from typing import Dict, List, Optional
from database import get_db
from repositories import generate_id, now_iso, row_to_dict, rows_to_list


def create_project(
    name: str,
    client_name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    status: str = "active"
) -> Dict:
    """Create new project"""
    import json
    
    project_id = generate_id("proj")
    now = now_iso()
    tags_json = json.dumps(tags) if tags else None
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (id, name, client_name, description, tags, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_id, name, client_name, description, tags_json, status, now, now))
    
    return get_project(project_id)


def get_project(project_id: str) -> Optional[Dict]:
    """Get project by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        return row_to_dict(row)


def list_projects(status: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """List projects"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT * FROM projects WHERE status = ? 
                ORDER BY created_at DESC LIMIT ?
            """, (status, limit))
        else:
            cursor.execute("""
                SELECT * FROM projects 
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))
        
        return rows_to_list(cursor.fetchall())


def update_project(
    project_id: str,
    name: Optional[str] = None,
    client_name: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    status: Optional[str] = None
) -> Optional[Dict]:
    """Update project"""
    import json
    
    # Get current project
    project = get_project(project_id)
    if not project:
        return None
    
    # Update fields
    if name is not None:
        project['name'] = name
    if client_name is not None:
        project['client_name'] = client_name
    if description is not None:
        project['description'] = description
    if tags is not None:
        project['tags'] = json.dumps(tags)
    if status is not None:
        project['status'] = status
    
    project['updated_at'] = now_iso()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects 
            SET name = ?, client_name = ?, description = ?, tags = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (
            project['name'], project['client_name'], project['description'],
            project['tags'], project['status'], project['updated_at'], project_id
        ))
    
    return get_project(project_id)


def delete_project(project_id: str) -> bool:
    """Delete project (cascades to all related data)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        return cursor.rowcount > 0


def get_project_stats(project_id: str) -> Dict:
    """Get project statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Count targets
        cursor.execute("SELECT COUNT(*) FROM targets WHERE project_id = ?", (project_id,))
        targets_count = cursor.fetchone()[0]
        
        # Count issues by severity
        cursor.execute("""
            SELECT severity, COUNT(*) as count 
            FROM issues 
            WHERE project_id = ? 
            GROUP BY severity
        """, (project_id,))
        issues_by_severity = {row['severity']: row['count'] for row in cursor.fetchall()}
        
        # Total issues
        cursor.execute("SELECT COUNT(*) FROM issues WHERE project_id = ?", (project_id,))
        total_issues = cursor.fetchone()[0]
        
        return {
            "targets_count": targets_count,
            "total_issues": total_issues,
            "issues_by_severity": issues_by_severity
        }
