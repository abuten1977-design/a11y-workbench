"""Database repository tests"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from repositories import projects, targets, sessions, issues

def test_create_and_get_project():
    project_id = projects.create({"name": "Test Project", "client": "Test client"})
    assert project_id is not None
    project = projects.get(project_id)
    assert project["name"] == "Test Project"

def test_list_projects():
    projects.create({"name": "Project 1"})
    projects.create({"name": "Project 2"})
    all_projects = projects.list()
    assert len(all_projects) >= 2

def test_create_and_get_target():
    project_id = projects.create({"name": "Test"})
    target_id = targets.create({
        "project_id": project_id,
        "name": "Login Page",
        "url": "https://example.com/login"
    })
    assert target_id is not None
    target = targets.get(target_id)
    assert target["name"] == "Login Page"

def test_list_targets_by_project():
    project_id = projects.create({"name": "Test"})
    targets.create({"project_id": project_id, "name": "Page 1", "url": "https://example.com/1"})
    targets.create({"project_id": project_id, "name": "Page 2", "url": "https://example.com/2"})
    project_targets = targets.list_by_project(project_id)
    assert len(project_targets) >= 2

def test_create_session():
    project_id = projects.create({"name": "Test"})
    target_id = targets.create({"project_id": project_id, "name": "Page", "url": "https://example.com"})
    session_id = sessions.create({
        "target_id": target_id,
        "screen_reader": "NVDA",
        "browser": "Firefox"
    })
    assert session_id is not None
    session = sessions.get(session_id)
    assert session["screen_reader"] == "NVDA"

def test_create_issue():
    project_id = projects.create({"name": "Test"})
    target_id = targets.create({"project_id": project_id, "name": "Page", "url": "https://example.com"})
    issue_id = issues.create({
        "target_id": target_id,
        "title": "Button missing label",
        "severity": "serious"
    })
    assert issue_id is not None
    issue = issues.get(issue_id)
    assert issue["title"] == "Button missing label"
