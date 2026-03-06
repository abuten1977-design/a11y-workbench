"""
Issues repository
"""
from typing import Dict, List, Optional
from database import get_db
from repositories import generate_id, now_iso, row_to_dict, rows_to_list


def create_issue(
    project_id: str,
    title: str,
    severity: str,
    target_id: Optional[str] = None,
    session_id: Optional[str] = None,
    finding_group_id: Optional[str] = None,
    raw_note: Optional[str] = None,
    description: Optional[str] = None,
    steps_to_reproduce: Optional[str] = None,
    observed_behavior: Optional[str] = None,
    expected_behavior: Optional[str] = None,
    user_impact: Optional[str] = None,
    confidence: str = "exact",
    affected_element: Optional[str] = None,
    wcag_criterion: Optional[str] = None,
    suggested_fix: Optional[str] = None,
    tags: Optional[List[str]] = None,
    source_type: str = "manual",
    status: str = "new"
) -> Dict:
    """Create new issue"""
    import json
    
    issue_id = generate_id("issue")
    now = now_iso()
    tags_json = json.dumps(tags) if tags else None
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO issues (
                id, project_id, target_id, session_id, finding_group_id,
                title, raw_note, description, steps_to_reproduce,
                observed_behavior, expected_behavior, user_impact,
                severity, confidence, affected_element, wcag_criterion,
                suggested_fix, tags, source_type, status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            issue_id, project_id, target_id, session_id, finding_group_id,
            title, raw_note, description, steps_to_reproduce,
            observed_behavior, expected_behavior, user_impact,
            severity, confidence, affected_element, wcag_criterion,
            suggested_fix, tags_json, source_type, status,
            now, now
        ))
    
    return get_issue(issue_id)


def get_issue(issue_id: str) -> Optional[Dict]:
    """Get issue by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
        row = cursor.fetchone()
        return row_to_dict(row)


def list_issues(
    project_id: Optional[str] = None,
    target_id: Optional[str] = None,
    session_id: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100
) -> List[Dict]:
    """List issues with filters"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM issues WHERE 1=1"
        params = []
        
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        if target_id:
            query += " AND target_id = ?"
            params.append(target_id)
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return rows_to_list(cursor.fetchall())


def update_issue(issue_id: str, **kwargs) -> Optional[Dict]:
    """Update issue fields"""
    import json
    
    issue = get_issue(issue_id)
    if not issue:
        return None
    
    # Update allowed fields
    allowed_fields = [
        'title', 'raw_note', 'description', 'steps_to_reproduce',
        'observed_behavior', 'expected_behavior', 'user_impact',
        'severity', 'confidence', 'affected_element', 'wcag_criterion',
        'suggested_fix', 'tags', 'status'
    ]
    
    for field in allowed_fields:
        if field in kwargs:
            value = kwargs[field]
            if field == 'tags' and value is not None:
                value = json.dumps(value)
            issue[field] = value
    
    issue['updated_at'] = now_iso()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE issues SET
                title = ?, raw_note = ?, description = ?, steps_to_reproduce = ?,
                observed_behavior = ?, expected_behavior = ?, user_impact = ?,
                severity = ?, confidence = ?, affected_element = ?, wcag_criterion = ?,
                suggested_fix = ?, tags = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (
            issue['title'], issue['raw_note'], issue['description'], issue['steps_to_reproduce'],
            issue['observed_behavior'], issue['expected_behavior'], issue['user_impact'],
            issue['severity'], issue['confidence'], issue['affected_element'], issue['wcag_criterion'],
            issue['suggested_fix'], issue['tags'], issue['status'], issue['updated_at'],
            issue_id
        ))
    
    return get_issue(issue_id)


def delete_issue(issue_id: str) -> bool:
    """Delete issue"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
        return cursor.rowcount > 0


def add_evidence(issue_id: str, evidence_type: str, content: str) -> Dict:
    """Add evidence to issue"""
    evidence_id = generate_id("evidence")
    now = now_iso()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO evidence (id, issue_id, type, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (evidence_id, issue_id, evidence_type, content, now))
    
    return {
        "id": evidence_id,
        "issue_id": issue_id,
        "type": evidence_type,
        "content": content,
        "created_at": now
    }


def get_issue_evidence(issue_id: str) -> List[Dict]:
    """Get all evidence for issue"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evidence WHERE issue_id = ? ORDER BY created_at", (issue_id,))
        return rows_to_list(cursor.fetchall())
