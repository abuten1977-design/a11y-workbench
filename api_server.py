#!/usr/bin/env python3
"""
A11y Workbench API Server v1.0
Project-based workflow
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import Optional, List
import sys
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from repositories import projects, targets, issues, evidence, sessions, finding_groups
from ai_service import AIService

# Инициализация AI Service
try:
    ai_service = AIService()
    print("✅ AI Service initialized")
except Exception as e:
    print(f"⚠️  AI Service not available: {e}")
    ai_service = None

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

class AIExpandRequest(BaseModel):
    raw_note: str
    html_code: Optional[str] = None
    project_id: Optional[str] = None
    session_id: Optional[str] = None
    target_url: Optional[str] = None

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
    session_id = sessions.create(data)
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

# ============= AI ENDPOINTS =============

@app.post("/api/v1/ai/expand")
async def ai_expand_note(data: AIExpandRequest):
    """
    Превратить короткую заметку в структурированный отчет
    
    Request:
    {
        "raw_note": "button unlabeled",
        "html_code": "<button>Submit</button>",  // optional
        "project_id": "proj_123",  // optional
        "session_id": "sess_456",  // optional
        "target_url": "https://example.com"  // optional
    }
    
    Response:
    {
        "success": true,
        "result": {
            "title": "...",
            "steps": [...],
            "observed": "...",
            "expected": "...",
            "impact": "...",
            "wcag": [...],
            "severity": "...",
            "fix": "...",
            "evidence_type": "..."
        },
        "processing_time": 2.3
    }
    """
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI Service not available")
    
    try:
        start_time = time.time()
        
        # Получить контекст если есть project_id
        context = {}
        if data.project_id:
            try:
                project = projects.get(data.project_id)
                context['project'] = project.get('name', 'Unknown')
            except:
                pass
        
        if data.target_url:
            context['target_url'] = data.target_url
        
        if data.session_id:
            try:
                session = sessions.get(data.session_id)
                context['tools'] = session.get('tools_used', '')
            except:
                pass
        
        # Вызвать AI
        result = await ai_service.expand_note(
            raw_note=data.raw_note,
            html_code=data.html_code,
            context=context if context else None
        )
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "result": result,
            "processing_time": round(processing_time, 2)
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

@app.get("/api/v1/ai/status")
async def ai_status():
    """Проверить статус AI Service"""
    if not ai_service:
        return {"available": False, "error": "AI Service not initialized"}
    
    return {
        "available": True,
        "model": ai_service.model,
        "rate_limit": f"{ai_service.max_requests_per_minute} requests/minute",
        "requests_in_last_minute": len(ai_service.request_times)
    }

@app.get("/api/v1/proxy")
async def proxy_url(url: str):
    """Proxy to fetch HTML from external URL (avoid CORS)"""
    import httpx
    
    # Trim whitespace from URL
    url = url.strip()
    
    # If URL is same server, use localhost to avoid external network
    url = url.replace('http://34.58.51.76:8000', 'http://localhost:8000')
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers={
                'User-Agent': 'A11y-Workbench/1.0'
            })
            return Response(
                content=response.text,
                media_type="text/html",
                status_code=response.status_code
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")

@app.get("/dashboard.js")
async def get_dashboard_js():
    """Serve dashboard JavaScript"""
    from pathlib import Path
    js_file = Path(__file__).parent / "dashboard.js"
    if js_file.exists():
        return Response(content=js_file.read_text(), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="dashboard.js not found")

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

# ============= EXPORTS =============

from exports import export_markdown, export_json, export_csv, get_statistics

@app.get("/api/v1/projects/{project_id}/export/markdown")
async def export_project_markdown(project_id: str):
    """Export project as Markdown report"""
    content = export_markdown(project_id)
    return Response(content=content, media_type="text/markdown")

@app.get("/api/v1/projects/{project_id}/export/json")
async def export_project_json(project_id: str):
    """Export project as JSON"""
    data = export_json(project_id)
    return data

@app.get("/api/v1/projects/{project_id}/export/csv")
async def export_project_csv(project_id: str):
    """Export project as CSV"""
    content = export_csv(project_id)
    return Response(content=content, media_type="text/csv")

@app.get("/api/v1/projects/{project_id}/statistics")
async def project_statistics(project_id: str):
    """Get project statistics"""
    stats = get_statistics(project_id)
    return stats

@app.get("/api/v1/statistics")
async def global_statistics():
    """Get global statistics"""
    stats = get_statistics()
    return stats

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
        .btn-primary { background: #0066cc; color: white; } /* Darker blue for better contrast */
        .btn-success { background: #28a745; color: white; }
        .btn-secondary { background: #6c757d; color: white; padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
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
        .stats-bar {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        }
        .stat-label {
            font-size: 12px;
            color: #aaa; /* Changed from #888 to #aaa for better contrast */
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 A11y Workbench</h1>
            
            <!-- Global Statistics -->
            <div id="global-stats" class="stats-bar"></div>
        </header>
        
        <main>
        <!-- Projects Section -->
        <section class="section">
            <h2>📁 Projects</h2>
            <button class="btn-primary" onclick="showCreateProject()">+ New Project</button>
            <div id="projects-list" class="list" style="margin-top: 15px;"></div>
        </section>
        
        <!-- Targets Section -->
        <section class="section hidden" id="targets-section">
            <h2>🎯 Targets / Pages</h2>
            <button class="btn-primary" onclick="showCreateTarget()">+ Add Target</button>
            <div id="targets-list" class="list" style="margin-top: 15px;"></div>
        </section>

        <!-- Sessions Section -->
        <section class="section hidden" id="sessions-section">
            <h2>🧪 Test Sessions</h2>
            <button class="btn-primary" onclick="showStartSession()">+ Start Session</button>
            <div id="sessions-list" class="list" style="margin-top: 15px;"></div>
            <div id="active-session" class="hidden" style="margin-top: 1rem; padding: 1rem; background: #1a3a1a; border-radius: 8px;">
                <strong>🟢 Active Session</strong>
                <div id="active-session-info" style="margin-top: 0.5rem; color: #aaa;"></div>
                <button class="btn-secondary" onclick="endSession()" style="margin-top: 0.5rem;">End Session</button>
            </div>
        </section>
        
        <!-- FindingGroups Section -->
        <section class="section hidden" id="groups-section">
            <h2>📂 Finding Groups</h2>
            <button class="btn-primary" onclick="showCreateGroup()">+ New Group</button>
            <div id="groups-list" class="list" style="margin-top: 15px;"></div>
        </section>
        
        <!-- Issues Section -->
        <section class="section hidden" id="issues-section">
            <h2>🐛 Issues</h2>
            <div style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
                <button class="btn-success" onclick="showCreateIssue()">+ Quick Capture</button>
                <button class="btn-primary" onclick="showDetailedIssue()">+ Detailed Issue</button>
            </div>
            
            <!-- Filters -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-bottom: 15px;">
                <input type="text" id="filter-search" placeholder="Search title..." style="padding: 8px; background: #333; border: 1px solid #444; border-radius: 6px; color: white;">
                <select id="filter-severity" onchange="loadIssues()" style="padding: 8px; background: #333; border: 1px solid #444; border-radius: 6px; color: white;">
                    <option value="">All Severities</option>
                    <option value="critical">Critical</option>
                    <option value="serious">Serious</option>
                    <option value="moderate">Moderate</option>
                    <option value="minor">Minor</option>
                </select>
                <select id="filter-status" onchange="loadIssues()" style="padding: 8px; background: #333; border: 1px solid #444; border-radius: 6px; color: white;">
                    <option value="">All Statuses</option>
                    <option value="new">New</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="fixed">Fixed</option>
                    <option value="wontfix">Won't Fix</option>
                </select>
                <button class="btn-primary" onclick="clearFilters()" style="padding: 8px;">Clear Filters</button>
            </div>
            
            <div id="issues-list" class="list"></div>
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
                <label>HTML Code (optional)</label>
                <textarea id="issue-html" placeholder="<button>Submit</button>" rows="3"></textarea>
                <div style="margin-top: 5px;">
                    <button type="button" class="btn-secondary" onclick="fetchPageHTML()">📥 Fetch HTML from target</button>
                    <label style="margin-left: 15px;">
                        <input type="checkbox" id="auto-fetch-html"> Auto-fetch HTML for AI
                    </label>
                </div>
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
            <button class="btn-primary" onclick="aiExpandNote()">🤖 AI Expand</button>
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
        
        <!-- Issue Detail Modal -->
        <div id="issue-modal" class="hidden" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; overflow-y: auto; padding: 20px;">
            <div style="max-width: 900px; margin: 0 auto; background: #2a2a2a; padding: 30px; border-radius: 8px;">
                <h2 id="modal-title" style="margin-bottom: 20px;"></h2>
                
                <div id="modal-content" style="margin-bottom: 30px;"></div>
                
                <h3 style="margin-bottom: 15px;">📎 Evidence</h3>
                <div id="evidence-list" style="margin-bottom: 20px;"></div>
                
                <div style="background: #1a1a1a; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
                    <h4 style="margin-bottom: 10px;">Add Evidence</h4>
                    <div class="form-group">
                        <label>Type</label>
                        <select id="evidence-type" onchange="updateEvidenceLabel()">
                            <option value="screen_reader_output">Screen Reader Output</option>
                            <option value="code">Code Snippet</option>
                            <option value="aria_dump">ARIA Info</option>
                            <option value="note">Notes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label id="evidence-content-label">Screen Reader Output</label>
                        <textarea id="evidence-content" placeholder="Paste screen reader output, code, or notes" style="min-height: 100px;"></textarea>
                    </div>
                    <button class="btn-success" onclick="addEvidence()">Add Evidence</button>
                </div>
                
                <button class="btn-danger" onclick="closeIssueModal()">Close</button>
            </div>
        </div>
    </div>

    <script src="/dashboard.js"></script>
    </main>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
