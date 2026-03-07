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

from repositories import projects, targets, issues, evidence, sessions, finding_groups

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
    session_id: Optional[str] = None
    finding_group_id: Optional[str] = None
    title: str
    raw_note: Optional[str] = None
    description: Optional[str] = None
    steps_to_reproduce: Optional[str] = None
    observed_behavior: Optional[str] = None
    expected_behavior: Optional[str] = None
    user_impact: Optional[str] = None
    severity: str = "moderate"
    confidence: Optional[str] = None
    affected_element: Optional[str] = None
    wcag_criterion: Optional[str] = None
    suggested_fix: Optional[str] = None
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

class FindingGroupCreate(BaseModel):
    project_id: str
    target_id: Optional[str] = None
    name: str
    category: str
    notes: Optional[str] = None

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

# Sessions
@app.get("/api/v1/projects/{project_id}/sessions")
async def list_sessions(project_id: str):
    items = sessions.list_by_project(project_id)
    return {"sessions": items, "total": len(items)}

@app.post("/api/v1/sessions")
async def create_session(data: dict):
    session_id = sessions.create(
        project_id=data['project_id'],
        target_id=data.get('target_id'),
        assistive_tech=data['assistive_tech'],
        browser=data['browser'],
        platform=data['platform'],
        tester_notes=data.get('tester_notes')
    )
    return {"id": session_id, "message": "Session started"}

@app.put("/api/v1/sessions/{session_id}/end")
async def end_session(session_id: str):
    success = sessions.end_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session ended"}

# FindingGroups
@app.get("/api/v1/projects/{project_id}/groups")
async def list_groups(project_id: str):
    items = finding_groups.list_by_project(project_id)
    return {"groups": items, "total": len(items)}

@app.post("/api/v1/groups")
async def create_group(data: FindingGroupCreate):
    group_id = finding_groups.create(data.dict())
    return {"id": group_id, "message": "Group created"}

@app.get("/api/v1/groups/{group_id}")
async def get_group(group_id: str):
    group = finding_groups.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

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

# WCAG
@app.get("/wcag_criteria_simple.json")
async def get_wcag():
    """Serve WCAG criteria JSON"""
    import json
    from pathlib import Path
    wcag_file = Path(__file__).parent / "wcag_criteria_simple.json"
    if wcag_file.exists():
        return JSONResponse(content=json.loads(wcag_file.read_text()))
    return JSONResponse(content=[])

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

        <!-- Sessions Section -->
        <div class="section hidden" id="sessions-section">
            <h2>🧪 Test Sessions</h2>
            <button class="btn-primary" onclick="showStartSession()">+ Start Session</button>
            <div id="sessions-list" class="list" style="margin-top: 15px;"></div>
            <div id="active-session" class="hidden" style="margin-top: 1rem; padding: 1rem; background: #1a3a1a; border-radius: 8px;">
                <strong>🟢 Active Session</strong>
                <div id="active-session-info" style="margin-top: 0.5rem; color: #888;"></div>
                <button class="btn-secondary" onclick="endSession()" style="margin-top: 0.5rem;">End Session</button>
            </div>
        </div>
        
        <!-- FindingGroups Section -->
        <div class="section hidden" id="groups-section">
            <h2>📂 Finding Groups</h2>
            <button class="btn-primary" onclick="showCreateGroup()">+ New Group</button>
            <div id="groups-list" class="list" style="margin-top: 15px;"></div>
        </div>
        
        <!-- Issues Section -->
        <div class="section hidden" id="issues-section">
            <h2>🐛 Issues</h2>
            <button class="btn-success" onclick="showCreateIssue()">+ Quick Capture</button>
            <button class="btn-primary" onclick="showDetailedIssue()" style="margin-left: 10px;">+ Detailed Issue</button>
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
        
        <!-- Start Session Form -->
        <div id="start-session-form" class="section hidden">
            <h2>Start Test Session</h2>
            <div class="form-group">
                <label>Target *</label>
                <select id="session-target-id">
                    <option value="">Select target...</option>
                </select>
            </div>
            <div class="form-group">
                <label>Assistive Tech *</label>
                <select id="session-at">
                    <option value="NVDA">NVDA</option>
                    <option value="JAWS">JAWS</option>
                    <option value="VoiceOver">VoiceOver</option>
                    <option value="TalkBack">TalkBack</option>
                    <option value="Narrator">Narrator</option>
                </select>
            </div>
            <div class="form-group">
                <label>Browser *</label>
                <select id="session-browser">
                    <option value="Chrome">Chrome</option>
                    <option value="Firefox">Firefox</option>
                    <option value="Edge">Edge</option>
                    <option value="Safari">Safari</option>
                </select>
            </div>
            <div class="form-group">
                <label>Platform *</label>
                <select id="session-platform">
                    <option value="Windows 11">Windows 11</option>
                    <option value="Windows 10">Windows 10</option>
                    <option value="macOS">macOS</option>
                    <option value="iOS">iOS</option>
                    <option value="Android">Android</option>
                </select>
            </div>
            <div class="form-group">
                <label>Notes</label>
                <textarea id="session-notes" placeholder="Optional"></textarea>
            </div>
            <button class="btn-success" onclick="startSession()">Start</button>
            <button class="btn-danger" onclick="hideStartSession()">Cancel</button>
        </div>
        
        <!-- Create Group Form -->
        <div id="create-group-form" class="section hidden">
            <h2>Create Finding Group</h2>
            <div class="form-group">
                <label>Name *</label>
                <input type="text" id="group-name" placeholder="e.g., Form Issues">
            </div>
            <div class="form-group">
                <label>Category *</label>
                <select id="group-category">
                    <option value="forms">Forms</option>
                    <option value="navigation">Navigation</option>
                    <option value="buttons">Buttons & Controls</option>
                    <option value="aria">ARIA</option>
                    <option value="focus">Focus Management</option>
                    <option value="semantics">Semantics</option>
                    <option value="images">Images & Media</option>
                    <option value="tables">Tables</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Notes</label>
                <textarea id="group-notes" placeholder="Optional"></textarea>
            </div>
            <button class="btn-success" onclick="createGroup()">Create</button>
            <button class="btn-danger" onclick="hideCreateGroup()">Cancel</button>
        </div>
        
        <!-- Create Issue Form -->
        <div id="create-issue-form" class="section hidden">
            <h2>Quick Capture Issue</h2>
            <div class="form-group">
                <label>Group (optional)</label>
                <select id="issue-group-id">
                    <option value="">No group</option>
                </select>
            </div>
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
        
        <!-- Detailed Issue Form -->
        <div id="detailed-issue-form" class="section hidden">
            <h2>Detailed Issue Report</h2>
            <div class="form-group">
                <label>Group (optional)</label>
                <select id="detailed-group-id">
                    <option value="">No group</option>
                </select>
            </div>
            <div class="form-group">
                <label>Title *</label>
                <input type="text" id="detailed-title" placeholder="e.g., Submit button not keyboard accessible">
            </div>
            <div class="form-group">
                <label>Steps to Reproduce</label>
                <textarea id="detailed-steps" placeholder="1. Navigate to checkout page&#10;2. Tab through form fields&#10;3. Try to reach submit button"></textarea>
            </div>
            <div class="form-group">
                <label>Observed Behavior</label>
                <textarea id="detailed-observed" placeholder="What actually happens"></textarea>
            </div>
            <div class="form-group">
                <label>Expected Behavior</label>
                <textarea id="detailed-expected" placeholder="What should happen"></textarea>
            </div>
            <div class="form-group">
                <label>User Impact</label>
                <textarea id="detailed-impact" placeholder="How this affects users with disabilities"></textarea>
            </div>
            <div class="form-group">
                <label>Affected Element</label>
                <input type="text" id="detailed-element" placeholder="e.g., .submit-btn or main form">
            </div>
            <div class="form-group">
                <label>WCAG Criterion</label>
                <select id="detailed-wcag">
                    <option value="">Select WCAG...</option>
                </select>
            </div>
            <div class="form-group">
                <label>Suggested Fix</label>
                <textarea id="detailed-fix" placeholder="How to fix this issue"></textarea>
            </div>
            <div class="form-group">
                <label>Severity *</label>
                <select id="detailed-severity">
                    <option value="minor">Minor</option>
                    <option value="moderate" selected>Moderate</option>
                    <option value="serious">Serious</option>
                    <option value="critical">Critical</option>
                </select>
            </div>
            <div class="form-group">
                <label>Confidence</label>
                <select id="detailed-confidence">
                    <option value="low">Low</option>
                    <option value="medium" selected>Medium</option>
                    <option value="high">High</option>
                </select>
            </div>
            <button class="btn-success" onclick="createDetailedIssue()">Create</button>
            <button class="btn-danger" onclick="hideDetailedIssue()">Cancel</button>
        </div>
    </div>

    <script>
        let currentProjectId = null;
        let currentTargetId = null;
        let activeSessionId = null;
        let wcagCriteria = [];
        
        // Load WCAG criteria on startup
        async function loadWCAG() {
            try {
                const wcagFile = await fetch('/wcag_criteria_simple.json');
                wcagCriteria = await wcagFile.json();
            } catch (err) {
                console.error('Failed to load WCAG:', err);
            }
        }
        
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
            document.getElementById('sessions-section').classList.remove('hidden');
            document.getElementById('groups-section').classList.remove('hidden');
            document.getElementById('issues-section').classList.remove('hidden');
            loadTargets();
            loadSessions();
            loadGroups();
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
        
        // Load sessions
        async function loadSessions() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/sessions`);
            const data = await res.json();
            
            const list = document.getElementById('sessions-list');
            if (data.sessions.length === 0) {
                list.innerHTML = '<div class="empty">No sessions yet. Start one!</div>';
            } else {
                list.innerHTML = data.sessions.map(s => {
                    const status = s.completed_at ? '✅ Completed' : '🟢 Active';
                    const duration = s.completed_at ? 
                        `${Math.round((new Date(s.completed_at) - new Date(s.started_at)) / 60000)} min` : 
                        'In progress';
                    return `
                        <div class="list-item">
                            <div>
                                <div class="list-item-title">${s.assistive_tech} + ${s.browser}</div>
                                <div class="list-item-meta">${status} • ${duration} • ${s.platform}</div>
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            // Check for active session
            const active = data.sessions.find(s => !s.completed_at);
            if (active) {
                activeSessionId = active.id;
                document.getElementById('active-session').classList.remove('hidden');
                document.getElementById('active-session-info').textContent = 
                    `${active.assistive_tech} + ${active.browser} on ${active.platform}`;
            } else {
                activeSessionId = null;
                document.getElementById('active-session').classList.add('hidden');
            }
        }
        
        // Load groups
        async function loadGroups() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            
            const list = document.getElementById('groups-list');
            if (data.groups.length === 0) {
                list.innerHTML = '<div class="empty">No groups yet. Create one!</div>';
            } else {
                list.innerHTML = data.groups.map(g => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${g.name}</div>
                            <div class="list-item-meta">${g.category}</div>
                        </div>
                    </div>
                `).join('');
            }
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
        async function showStartSession() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            if (activeSessionId) {
                alert('End current session first!');
                return;
            }
            
            // Load targets into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/targets`);
            const data = await res.json();
            const select = document.getElementById('session-target-id');
            select.innerHTML = '<option value="">Select target...</option>' + 
                data.targets.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
            
            document.getElementById('start-session-form').classList.remove('hidden');
        }
        function hideStartSession() {
            document.getElementById('start-session-form').classList.add('hidden');
        }
        function showCreateGroup() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            document.getElementById('create-group-form').classList.remove('hidden');
        }
        function hideCreateGroup() {
            document.getElementById('create-group-form').classList.add('hidden');
        }
        async function showCreateIssue() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            
            // Load groups into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            const select = document.getElementById('issue-group-id');
            select.innerHTML = '<option value="">No group</option>' + 
                data.groups.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
            
            document.getElementById('create-issue-form').classList.remove('hidden');
        }
        function hideCreateIssue() {
            document.getElementById('create-issue-form').classList.add('hidden');
        }
        async function showDetailedIssue() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            
            // Load groups into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            const select = document.getElementById('detailed-group-id');
            select.innerHTML = '<option value="">No group</option>' + 
                data.groups.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
            
            // Load WCAG into dropdown
            const wcagSelect = document.getElementById('detailed-wcag');
            wcagSelect.innerHTML = '<option value="">Select WCAG...</option>' + 
                wcagCriteria.map(c => `<option value="${c.id}">${c.id} - ${c.title}</option>`).join('');
            
            document.getElementById('detailed-issue-form').classList.remove('hidden');
        }
        function hideDetailedIssue() {
            document.getElementById('detailed-issue-form').classList.add('hidden');
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
        
        // Start session
        async function startSession() {
            const targetId = document.getElementById('session-target-id').value;
            const at = document.getElementById('session-at').value;
            const browser = document.getElementById('session-browser').value;
            const platform = document.getElementById('session-platform').value;
            
            if (!targetId) {
                alert('Select a target!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: targetId,
                assistive_tech: at,
                browser: browser,
                platform: platform,
                tester_notes: document.getElementById('session-notes').value || null
            };
            
            const res = await fetch('/api/v1/sessions', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideStartSession();
                document.getElementById('session-notes').value = '';
                loadSessions();
            }
        }
        
        // End session
        async function endSession() {
            if (!activeSessionId) return;
            
            const res = await fetch(`/api/v1/sessions/${activeSessionId}/end`, {
                method: 'PUT'
            });
            
            if (res.ok) {
                loadSessions();
            }
        }
        
        // Create group
        async function createGroup() {
            const name = document.getElementById('group-name').value;
            if (!name) {
                alert('Group name required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                name,
                category: document.getElementById('group-category').value,
                notes: document.getElementById('group-notes').value || null
            };
            
            const res = await fetch('/api/v1/groups', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateGroup();
                document.getElementById('group-name').value = '';
                document.getElementById('group-notes').value = '';
                loadGroups();
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
                finding_group_id: document.getElementById('issue-group-id').value || null,
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
        
        // Create detailed issue
        async function createDetailedIssue() {
            const title = document.getElementById('detailed-title').value;
            if (!title) {
                alert('Title required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                session_id: activeSessionId,
                finding_group_id: document.getElementById('detailed-group-id').value || null,
                title,
                steps_to_reproduce: document.getElementById('detailed-steps').value || null,
                observed_behavior: document.getElementById('detailed-observed').value || null,
                expected_behavior: document.getElementById('detailed-expected').value || null,
                user_impact: document.getElementById('detailed-impact').value || null,
                affected_element: document.getElementById('detailed-element').value || null,
                wcag_criterion: document.getElementById('detailed-wcag').value || null,
                suggested_fix: document.getElementById('detailed-fix').value || null,
                severity: document.getElementById('detailed-severity').value,
                confidence: document.getElementById('detailed-confidence').value,
                source_type: 'manual',
                status: 'new'
            };
            
            const res = await fetch('/api/v1/issues', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideDetailedIssue();
                // Clear form
                document.getElementById('detailed-title').value = '';
                document.getElementById('detailed-steps').value = '';
                document.getElementById('detailed-observed').value = '';
                document.getElementById('detailed-expected').value = '';
                document.getElementById('detailed-impact').value = '';
                document.getElementById('detailed-element').value = '';
                document.getElementById('detailed-fix').value = '';
                loadIssues();
            }
        }
        
        // Load on start
        loadWCAG();
        loadProjects();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
