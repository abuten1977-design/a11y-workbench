#!/usr/bin/env python3
"""
Test repositories
"""
from repositories.projects import create_project, get_project, list_projects, get_project_stats
from repositories.issues import create_issue, get_issue, list_issues, add_evidence, get_issue_evidence

print("🧪 Testing repositories...")
print("=" * 50)

# Test 1: Create project
print("\n1️⃣ Creating project...")
project = create_project(
    name="Test Project",
    client_name="Test Client",
    description="Test description",
    tags=["test", "demo"]
)
print(f"✅ Created project: {project['id']}")
print(f"   Name: {project['name']}")

# Test 2: Get project
print("\n2️⃣ Getting project...")
fetched = get_project(project['id'])
print(f"✅ Fetched project: {fetched['name']}")

# Test 3: List projects
print("\n3️⃣ Listing projects...")
projects = list_projects()
print(f"✅ Found {len(projects)} projects")

# Test 4: Create issue
print("\n4️⃣ Creating issue...")
issue = create_issue(
    project_id=project['id'],
    title="Test Issue",
    severity="serious",
    raw_note="Button unlabeled",
    description="Submit button has no label",
    wcag_criterion="4.1.2",
    tags=["button", "forms"]
)
print(f"✅ Created issue: {issue['id']}")
print(f"   Title: {issue['title']}")

# Test 5: Add evidence
print("\n5️⃣ Adding evidence...")
evidence = add_evidence(
    issue_id=issue['id'],
    evidence_type="screen_reader_output",
    content="NVDA: button"
)
print(f"✅ Added evidence: {evidence['id']}")

# Test 6: Get evidence
print("\n6️⃣ Getting evidence...")
all_evidence = get_issue_evidence(issue['id'])
print(f"✅ Found {len(all_evidence)} evidence items")

# Test 7: List issues
print("\n7️⃣ Listing issues...")
issues = list_issues(project_id=project['id'])
print(f"✅ Found {len(issues)} issues")

# Test 8: Project stats
print("\n8️⃣ Getting project stats...")
stats = get_project_stats(project['id'])
print(f"✅ Stats:")
print(f"   Total issues: {stats['total_issues']}")
print(f"   By severity: {stats['issues_by_severity']}")

print("\n" + "=" * 50)
print("✅ All tests passed!")
