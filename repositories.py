"""
Repositories for all entities
"""
from typing import List, Dict, Any, Optional
from repository import BaseRepository
from database import db


class ProjectRepository(BaseRepository):
    """Projects repository"""
    table_name = "projects"
    id_prefix = "proj"
    
    def list_by_status(self, status: str) -> List[Dict[str, Any]]:
        """List projects by status"""
        query = f"SELECT * FROM {self.table_name} WHERE status = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (status,))
        return [dict(row) for row in rows]


class TargetRepository(BaseRepository):
    """Targets repository"""
    table_name = "targets"
    id_prefix = "target"
    
    def list_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """List targets for project"""
        query = f"SELECT * FROM {self.table_name} WHERE project_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (project_id,))
        return [dict(row) for row in rows]


class TestSessionRepository(BaseRepository):
    """Test sessions repository"""
    table_name = "test_sessions"
    id_prefix = "session"
    
    def list_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """List sessions for project"""
        query = f"SELECT * FROM {self.table_name} WHERE project_id = ? ORDER BY started_at DESC"
        rows = db.fetchall(query, (project_id,))
        return [dict(row) for row in rows]
    
    def list_by_target(self, target_id: str) -> List[Dict[str, Any]]:
        """List sessions for target"""
        query = f"SELECT * FROM {self.table_name} WHERE target_id = ? ORDER BY started_at DESC"
        rows = db.fetchall(query, (target_id,))
        return [dict(row) for row in rows]
    
    def end_session(self, session_id: str) -> bool:
        """End session by setting completed_at"""
        from datetime import datetime
        query = f"UPDATE {self.table_name} SET completed_at = ? WHERE id = ?"
        result = db.execute(query, (datetime.now().isoformat(), session_id))
        return result > 0


class FindingGroupRepository(BaseRepository):
    """Finding groups repository"""
    table_name = "finding_groups"
    id_prefix = "group"
    
    def list_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """List groups for project"""
        query = f"SELECT * FROM {self.table_name} WHERE project_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (project_id,))
        return [dict(row) for row in rows]


class IssueRepository(BaseRepository):
    """Issues repository"""
    table_name = "issues"
    id_prefix = "issue"
    
    def list_by_project(self, project_id: str, 
                       severity: Optional[str] = None,
                       status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List issues for project with filters"""
        query = f"SELECT * FROM {self.table_name} WHERE project_id = ?"
        params = [project_id]
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        rows = db.fetchall(query, tuple(params))
        return [dict(row) for row in rows]
    
    def list_by_target(self, target_id: str) -> List[Dict[str, Any]]:
        """List issues for target"""
        query = f"SELECT * FROM {self.table_name} WHERE target_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (target_id,))
        return [dict(row) for row in rows]
    
    def list_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """List issues for session"""
        query = f"SELECT * FROM {self.table_name} WHERE session_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (session_id,))
        return [dict(row) for row in rows]


class EvidenceRepository(BaseRepository):
    """Evidence repository"""
    table_name = "evidence"
    id_prefix = "evidence"
    
    def list_by_issue(self, issue_id: str) -> List[Dict[str, Any]]:
        """List evidence for issue"""
        query = f"SELECT * FROM {self.table_name} WHERE issue_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (issue_id,))
        return [dict(row) for row in rows]


class ChecklistRepository(BaseRepository):
    """Checklists repository"""
    table_name = "checklists"
    id_prefix = "checklist"
    
    def list_by_category(self, category: str) -> List[Dict[str, Any]]:
        """List checklists by category"""
        query = f"SELECT * FROM {self.table_name} WHERE category = ? ORDER BY name"
        rows = db.fetchall(query, (category,))
        return [dict(row) for row in rows]


class ChecklistResultRepository(BaseRepository):
    """Checklist results repository"""
    table_name = "checklist_results"
    id_prefix = "result"
    
    def list_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """List results for session"""
        query = f"SELECT * FROM {self.table_name} WHERE session_id = ? ORDER BY created_at"
        rows = db.fetchall(query, (session_id,))
        return [dict(row) for row in rows]


class TemplateRepository(BaseRepository):
    """Templates repository"""
    table_name = "templates"
    id_prefix = "template"
    
    def list_by_category(self, category: str) -> List[Dict[str, Any]]:
        """List templates by category"""
        query = f"SELECT * FROM {self.table_name} WHERE category = ? ORDER BY name"
        rows = db.fetchall(query, (category,))
        return [dict(row) for row in rows]


class ExportRepository(BaseRepository):
    """Exports repository"""
    table_name = "exports"
    id_prefix = "export"
    
    def list_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """List exports for project"""
        query = f"SELECT * FROM {self.table_name} WHERE project_id = ? ORDER BY created_at DESC"
        rows = db.fetchall(query, (project_id,))
        return [dict(row) for row in rows]


# Repository instances
projects = ProjectRepository()
targets = TargetRepository()
sessions = TestSessionRepository()
finding_groups = FindingGroupRepository()
issues = IssueRepository()
evidence = EvidenceRepository()
checklists = ChecklistRepository()
checklist_results = ChecklistResultRepository()
templates = TemplateRepository()
exports = ExportRepository()
