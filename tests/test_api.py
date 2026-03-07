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
    assert "id" in response.json()
    assert response.json()["message"] == "Project created"

def test_get_projects():
    client.post("/api/v1/projects", json={"name": "Project 1"})
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 1
    assert projects[0]["name"] == "Project 1"

def test_create_target():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    response = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Login Page",
        "url": "https://example.com/login"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_session():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    response = client.post("/api/v1/sessions", json={
        "target_id": target_id,
        "screen_reader": "NVDA",
        "browser": "Firefox"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_issue():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    response = client.post("/api/v1/issues", json={
        "target_id": target_id,
        "title": "Button missing label",
        "severity": "serious"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_issues():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    client.post("/api/v1/issues", json={
        "target_id": target_id,
        "title": "Critical issue",
        "severity": "critical"
    })
    
    # Get issues for project
    response = client.get(f"/api/v1/projects/{proj['id']}/issues")
    assert response.status_code == 200
    issues = response.json()
    assert len(issues) >= 1

def test_add_evidence():
    proj = client.post("/api/v1/projects", json={"name": "Test"}).json()
    target_resp = client.post("/api/v1/targets", json={
        "project_id": proj["id"],
        "name": "Page",
        "url": "https://example.com"
    })
    target_id = target_resp.json()["id"]
    
    issue_resp = client.post("/api/v1/issues", json={
        "target_id": target_id,
        "title": "Issue",
        "severity": "moderate"
    })
    issue_id = issue_resp.json()["id"]
    
    response = client.post("/api/v1/evidence", json={
        "issue_id": issue_id,
        "evidence_type": "screen_reader_output",
        "content": "Button, unlabeled"
    })
    assert response.status_code == 200
    assert "id" in response.json()
