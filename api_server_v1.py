#!/usr/bin/env python3
"""
A11y Workbench API Server v1.0
Project-based workflow
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from repositories import projects, targets, issues, evidence

app = FastAPI(
    title="A11y Workbench API",
    description="Accessibility testing workflow system",
    version="1.0.0"
)

# ============= MODELS =============

class ProjectCreate(BaseModel):
    name: str
    client_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    status: str = "active"

class TargetCreate(BaseModel):
    project_id: str
    name: str
    url: str
    flow_type: str = "page"
    notes: Optional[str] = None

class IssueCreate(BaseModel):
    project_id: str
    target_id: Optional[str] = None
    title: str
    raw_note: Optional[str] = None
    description: Optional[str] = None
    severity: str = "moderate"
    source_type: str = "manual"
    status: str = "new"

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    steps_to_reproduce: Optional[str] = None
    observed_behavior: Optional[str] = None
    expected_behavior: Optional[str] = None
    user_impact: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    wcag_criterion: Optional[str] = None
    suggested_fix: Optional[str] = None
    affected_element: Optional[str] = None

class EvidenceCreate(BaseModel):
    issue_id: str
    type: str
    content: str

# ============= API ENDPOINTS =============

@app.get("/")
async def root():
    return {
        "service": "A11y Workbench",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Projects
@app.get("/api/v1/projects")
async def list_projects(status: Optional[str] = None):
    if status:
        items = projects.list_by_status(status)
    else:
        items = projects.list_all()
    return {"projects": items, "total": len(items)}

@app.post("/api/v1/projects")
async def create_project(data: ProjectCreate):
    project_id = projects.create(data.dict())
    return {"id": project_id, "message": "Project created"}

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    project = projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: str):
    success = projects.delete(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted"}

# Targets
@app.get("/api/v1/projects/{project_id}/targets")
async def list_targets(project_id: str):
    items = targets.list_by_project(project_id)
    return {"targets": items, "total": len(items)}

@app.post("/api/v1/targets")
async def create_target(data: TargetCreate):
    target_id = targets.create(data.dict())
    return {"id": target_id, "message": "Target created"}

@app.get("/api/v1/targets/{target_id}")
async def get_target(target_id: str):
    target = targets.get(target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

# Issues
@app.get("/api/v1/projects/{project_id}/issues")
async def list_issues(project_id: str, severity: Optional[str] = None, status: Optional[str] = None):
    items = issues.list_by_project(project_id, severity=severity, status=status)
    return {"issues": items, "total": len(items)}

@app.post("/api/v1/issues")
async def create_issue(data: IssueCreate):
    issue_id = issues.create(data.dict())
    return {"id": issue_id, "message": "Issue created"}

@app.get("/api/v1/issues/{issue_id}")
async def get_issue(issue_id: str):
    issue = issues.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Get evidence
    issue_evidence = evidence.list_by_issue(issue_id)
    issue['evidence'] = issue_evidence
    
    return issue

@app.put("/api/v1/issues/{issue_id}")
async def update_issue(issue_id: str, data: IssueUpdate):
    # Filter out None values
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    
    success = issues.update(issue_id, update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return {"message": "Issue updated"}

@app.delete("/api/v1/issues/{issue_id}")
async def delete_issue(issue_id: str):
    success = issues.delete(issue_id)
    if not success:
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"message": "Issue deleted"}

# Evidence
@app.post("/api/v1/evidence")
async def create_evidence(data: EvidenceCreate):
    evidence_id = evidence.create(data.dict())
    return {"id": evidence_id, "message": "Evidence created"}

@app.get("/api/v1/issues/{issue_id}/evidence")
async def list_evidence(issue_id: str):
    items = evidence.list_by_issue(issue_id)
    return {"evidence": items, "total": len(items)}

# ============= DASHBOARD =============

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A11y Workbench</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { margin-bottom: 30px; }
        
        .section {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .section h2 { margin-bottom: 15px; font-size: 18px; }
        
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .btn-primary { background: #4a9eff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        
        .list { display: flex; flex-direction: column; gap: 10px; }
        .list-item {
            background: #333;
            padding: 15px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .list-item-title { font-size: 16px; font-weight: bold; }
        .list-item-meta { font-size: 12px; opacity: 0.7; margin-top: 5px; }
        
        .empty { text-align: center; opacity: 0.5; padding: 40px; }
        
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 10px;
            background: #333;
            border: 1px solid #444;
            border-radius: 6px;
            color: white;
            font-size: 14px;
        }
        .form-group textarea {
            min-height: 80px;
            resize: vertical;
        }
        
        .hidden { display: none; }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .badge-critical { background: #dc3545; }
        .badge-serious { background: #ff6b6b; }
        .badge-moderate { background: #ffc107; color: #000; }
        .badge-minor { background: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 A11y Workbench</h1>
        
        <!-- Projects Section -->
        <div class="section">
            <h2>📁 Projects</h2>
            <button class="btn-primary" onclick="showCreateProject()">+ New Project</button>
            <div id="projects-list" class="list" style="margin-top: 15px;"></div>
        </div>
        
        <!-- Targets Section -->
        <div class="section hidden" id="targets-section">
            <h2>🎯 Targets / Pages</h2>
            <button class="btn-primary" onclick="showCreateTarget()">+ Add Target</button>
            <div id="targets-list" class="list" style="margin-top: 15px;"></div>
        </div>
        
        <!-- Issues Section -->
        <div class="section hidden" id="issues-section">
            <h2>🐛 Issues</h2>
            <button class="btn-success" onclick="showCreateIssue()">+ Quick Capture</button>
            <div id="issues-list" class="list" style="margin-top: 15px;"></div>
        </div>
        
        <!-- Create Project Form -->
        <div id="create-project-form" class="section hidden">
            <h2>Create Project</h2>
            <div class="form-group">
                <label>Project Name *</label>
                <input type="text" id="project-name" placeholder="e.g., Acme Corp Website">
            </div>
            <div class="form-group">
                <label>Client Name</label>
                <input type="text" id="project-client" placeholder="Optional">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="project-description" placeholder="Optional"></textarea>
            </div>
            <button class="btn-success" onclick="createProject()">Create</button>
            <button class="btn-danger" onclick="hideCreateProject()">Cancel</button>
        </div>
        
        <!-- Create Target Form -->
        <div id="create-target-form" class="section hidden">
            <h2>Add Target / Page</h2>
            <div class="form-group">
                <label>Name *</label>
                <input type="text" id="target-name" placeholder="e.g., Checkout Page">
            </div>
            <div class="form-group">
                <label>URL *</label>
                <input type="text" id="target-url" placeholder="https://example.com/checkout">
            </div>
            <div class="form-group">
                <label>Flow Type</label>
                <select id="target-flow-type">
                    <option value="page">Page</option>
                    <option value="form">Form</option>
                    <option value="checkout">Checkout</option>
                    <option value="auth">Auth (Login/Signup)</option>
                    <option value="menu">Menu</option>
                    <option value="modal">Modal</option>
                    <option value="search">Search</option>
                    <option value="table">Table</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Notes</label>
                <textarea id="target-notes" placeholder="Optional"></textarea>
            </div>
            <button class="btn-success" onclick="createTarget()">Create</button>
            <button class="btn-danger" onclick="hideCreateTarget()">Cancel</button>
        </div>
        
        <!-- Create Issue Form -->
        <div id="create-issue-form" class="section hidden">
            <h2>Quick Capture Issue</h2>
            <div class="form-group">
                <label>Title *</label>
                <input type="text" id="issue-title" placeholder="e.g., Button unlabeled">
            </div>
            <div class="form-group">
                <label>Raw Note</label>
                <textarea id="issue-note" placeholder="Quick description"></textarea>
            </div>
            <div class="form-group">
                <label>Severity</label>
                <select id="issue-severity">
                    <option value="minor">Minor</option>
                    <option value="moderate" selected>Moderate</option>
                    <option value="serious">Serious</option>
                    <option value="critical">Critical</option>
                </select>
            </div>
            <button class="btn-success" onclick="createIssue()">Create</button>
            <button class="btn-danger" onclick="hideCreateIssue()">Cancel</button>
        </div>
    </div>

    <script>
        let currentProjectId = null;
        let currentTargetId = null;
        
        // Load projects
        async function loadProjects() {
            const res = await fetch('/api/v1/projects');
            const data = await res.json();
            
            const list = document.getElementById('projects-list');
            if (data.projects.length === 0) {
                list.innerHTML = '<div class="empty">No projects yet. Create one!</div>';
            } else {
                list.innerHTML = data.projects.map(p => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${p.name}</div>
                            <div class="list-item-meta">${p.client_name || 'No client'} • ${p.status}</div>
                        </div>
                        <button class="btn-primary" onclick="selectProject('${p.id}')">Open</button>
                    </div>
                `).join('');
            }
        }
        
        // Select project
        async function selectProject(projectId) {
            currentProjectId = projectId;
            document.getElementById('targets-section').classList.remove('hidden');
            document.getElementById('issues-section').classList.remove('hidden');
            loadTargets();
            loadIssues();
        }
        
        // Load targets
        async function loadTargets() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/targets`);
            const data = await res.json();
            
            const list = document.getElementById('targets-list');
            if (data.targets.length === 0) {
                list.innerHTML = '<div class="empty">No targets yet. Add one!</div>';
            } else {
                list.innerHTML = data.targets.map(t => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${t.name}</div>
                            <div class="list-item-meta">${t.url} • ${t.flow_type}</div>
                        </div>
                        <button class="btn-primary" onclick="selectTarget('${t.id}')">Select</button>
                    </div>
                `).join('');
            }
        }
        
        // Select target
        function selectTarget(targetId) {
            currentTargetId = targetId;
            alert('Target selected! Now issues will be linked to this target.');
        }
        
        // Load issues
        async function loadIssues() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/issues`);
            const data = await res.json();
            
            const list = document.getElementById('issues-list');
            if (data.issues.length === 0) {
                list.innerHTML = '<div class="empty">No issues yet. Create one!</div>';
            } else {
                list.innerHTML = data.issues.map(i => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${i.title}</div>
                            <div class="list-item-meta">
                                <span class="badge badge-${i.severity}">${i.severity}</span>
                                ${i.wcag_criterion || 'No WCAG'}
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        }
        
        // Show/hide forms
        function showCreateProject() {
            document.getElementById('create-project-form').classList.remove('hidden');
        }
        function hideCreateProject() {
            document.getElementById('create-project-form').classList.add('hidden');
        }
        function showCreateTarget() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            document.getElementById('create-target-form').classList.remove('hidden');
        }
        function hideCreateTarget() {
            document.getElementById('create-target-form').classList.add('hidden');
        }
        function showCreateIssue() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            document.getElementById('create-issue-form').classList.remove('hidden');
        }
        function hideCreateIssue() {
            document.getElementById('create-issue-form').classList.add('hidden');
        }
        
        // Create project
        async function createProject() {
            const name = document.getElementById('project-name').value;
            if (!name) {
                alert('Project name required!');
                return;
            }
            
            const data = {
                name,
                client_name: document.getElementById('project-client').value || null,
                description: document.getElementById('project-description').value || null
            };
            
            const res = await fetch('/api/v1/projects', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateProject();
                document.getElementById('project-name').value = '';
                document.getElementById('project-client').value = '';
                document.getElementById('project-description').value = '';
                loadProjects();
            }
        }
        
        // Create target
        async function createTarget() {
            const name = document.getElementById('target-name').value;
            const url = document.getElementById('target-url').value;
            
            if (!name || !url) {
                alert('Name and URL required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                name,
                url,
                flow_type: document.getElementById('target-flow-type').value,
                notes: document.getElementById('target-notes').value || null
            };
            
            const res = await fetch('/api/v1/targets', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateTarget();
                document.getElementById('target-name').value = '';
                document.getElementById('target-url').value = '';
                document.getElementById('target-notes').value = '';
                loadTargets();
            }
        }
        
        // Create issue
        async function createIssue() {
            const title = document.getElementById('issue-title').value;
            if (!title) {
                alert('Title required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                title,
                raw_note: document.getElementById('issue-note').value || null,
                severity: document.getElementById('issue-severity').value
            };
            
            const res = await fetch('/api/v1/issues', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateIssue();
                document.getElementById('issue-title').value = '';
                document.getElementById('issue-note').value = '';
                loadIssues();
            }
        }
        
        // Load on start
        loadProjects();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
