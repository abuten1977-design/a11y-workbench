"""API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api_server_v1 import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_project():
    response = client.post("/api/v1/projects", json={"name": "Test Project"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["message"] == "Project created"

def test_get_projects():
    # Create project
    proj_resp = client.post("/api/v1/projects", json={"name": "Project 1"})
    proj_id = proj_resp.json()["id"]
    
    # Get all projects
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 1
    
    # Get specific project
    proj = client.get(f"/api/v1/projects/{proj_id}")
    assert proj.status_code == 200
    assert proj.json()["name"] == "Project 1"

def test_create_target():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    response = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Login Page",
        "url": "https://example.com/login"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Target created"

def test_list_targets():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page 1",
        "url": "https://example.com/1"
    })
    
    response = client.get(f"/api/v1/projects/{proj['id']}/targets")
    assert response.status_code == 200
    data = response.json()
    assert "targets" in data
    assert data["total"] >= 1

def test_create_session():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    response = client.post("/api/v1/sessions", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "assistive_tech": "NVDA",
        "browser": "Firefox",
        "platform": "Windows 11"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Session started"

def test_create_issue():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    response = client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Button missing label",
        "severity": "serious"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["message"] == "Issue created"

def test_list_issues():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Critical issue",
        "severity": "critical"
    })
    
    response = client.get(f"/api/v1/projects/{proj['id']}/issues")
    assert response.status_code == 200
    data = response.json()
    assert "issues" in data
    assert data["total"] >= 1

def test_add_evidence():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    issue_resp = client.post("/api/v1/issues", json={
        "project_id": proj["id"],
        "target_id": target_id,
        "title": "Issue",
        "severity": "moderate"
    })
    issue_id = issue_resp.json()["id"]
    
    response = client.post("/api/v1/evidence", json={
        "issue_id": issue_id,
        "type": "screen_reader_output",
        "content": "Button, unlabeled"
    })
    assert response.status_code == 200
    assert "id" in response.json()
