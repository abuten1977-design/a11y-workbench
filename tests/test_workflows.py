"""End-to-end workflow tests"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api_server_v1 import app

client = TestClient(app)

def test_complete_testing_workflow():
    """Test: Create project → target → session → issue → evidence"""
    # 1. Create project
    proj = client.post("/api/v1/projects", json={"name": "Client Website"}).json()
    assert "id" in proj
    
    # 2. Create target
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Login Form",
        "url": "https://example.com/login"
    })
    assert target_resp.status_code == 200
    target_id = target_resp.json()["id"]
    
    # 3. Start session
    session_resp = client.post("/api/v1/sessions", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "assistive_tech": "NVDA",
        "browser": "Firefox",
        "platform": "Windows 11"
    })
    assert session_resp.status_code == 200
    
    # 4. Create issue
    issue_resp = client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Submit button missing accessible name",
        "severity": "serious"
    })
    assert issue_resp.status_code == 200
    issue_id = issue_resp.json()["id"]
    
    # 5. Add evidence
    evidence_resp = client.post("/api/v1/evidence", json={
        "issue_id": issue_id,
        "type": "screen_reader_output",
        "content": "Button, unlabeled"
    })
    assert evidence_resp.status_code == 200
    
    # 6. Verify issues exist
    issues_resp = client.get(f"/api/v1/projects/{proj['id']}/issues")
    assert issues_resp.status_code == 200
    data = issues_resp.json()
    assert data["total"] >= 1

def test_multiple_projects_workflow():
    """Test: Multiple projects with targets and issues"""
    # Create 2 projects
    proj1 = client.post("/api/v1/projects", json={"name": "Project A"}).json()
    proj2 = client.post("/api/v1/projects", json={"name": "Project B"}).json()
    
    # Add targets to each
    target1_resp = client.post("/api/v1/targets", json={
        "project_id": proj1["id"],
        "name": "Page 1",
        "url": "https://a.com"
    })
    target1_id = target1_resp.json()["id"]
    
    target2_resp = client.post("/api/v1/targets", json={
        "project_id": proj2["id"],
        "name": "Page 2",
        "url": "https://b.com"
    })
    target2_id = target2_resp.json()["id"]
    
    # Add issues
    client.post("/api/v1/issues", json={
        "project_id": proj1["id"],
        "target_id": target1_id,
        "title": "Issue A",
        "severity": "critical"
    })
    client.post("/api/v1/issues", json={
        "project_id": proj2["id"],
        "target_id": target2_id,
        "title": "Issue B",
        "severity": "moderate"
    })
    
    # Verify both projects have issues
    issues1 = client.get(f"/api/v1/projects/{proj1['id']}/issues").json()
    issues2 = client.get(f"/api/v1/projects/{proj2['id']}/issues").json()
    assert issues1["total"] >= 1
    assert issues2["total"] >= 1

def test_filtering_issues():
    """Test: Filter issues by severity"""
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    # Create issues with different severities
    client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Critical issue",
        "severity": "critical"
    })
    client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Moderate issue",
        "severity": "moderate"
    })
    
    # Filter by severity
    critical = client.get(f"/api/v1/projects/{proj['id']}/issues?severity=critical").json()
    all_issues = client.get(f"/api/v1/projects/{proj['id']}/issues").json()
    
    assert critical["total"] == 1
    assert all_issues["total"] >= 2
