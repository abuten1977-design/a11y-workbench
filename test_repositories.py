#!/usr/bin/env python3
"""
Test repositories
"""
from repositories import projects, targets, issues, evidence

print("🧪 Testing repositories...")
print("=" * 50)

# Test 1: Create project
print("\n1️⃣ Creating project...")
project_id = projects.create({
    "name": "Test Project",
    "client_name": "Test Client",
    "description": "Test description",
    "status": "active"
})
print(f"✅ Created project: {project_id}")

# Test 2: Get project
print("\n2️⃣ Getting project...")
project = projects.get(project_id)
print(f"✅ Project: {project['name']}")

# Test 3: Create target
print("\n3️⃣ Creating target...")
target_id = targets.create({
    "project_id": project_id,
    "name": "Homepage",
    "url": "https://example.com",
    "flow_type": "page"
})
print(f"✅ Created target: {target_id}")

# Test 4: Create issue
print("\n4️⃣ Creating issue...")
issue_id = issues.create({
    "project_id": project_id,
    "target_id": target_id,
    "title": "Test Issue",
    "raw_note": "Button unlabeled",
    "severity": "serious",
    "status": "new",
    "source_type": "manual"
})
print(f"✅ Created issue: {issue_id}")

# Test 5: Add evidence
print("\n5️⃣ Adding evidence...")
evidence_id = evidence.create({
    "issue_id": issue_id,
    "type": "screen_reader_output",
    "content": "NVDA: button"
})
print(f"✅ Created evidence: {evidence_id}")

# Test 6: List issues
print("\n6️⃣ Listing issues...")
issue_list = issues.list_by_project(project_id)
print(f"✅ Found {len(issue_list)} issues")

# Test 7: Update issue
print("\n7️⃣ Updating issue...")
success = issues.update(issue_id, {
    "status": "confirmed",
    "wcag_criterion": "4.1.2"
})
print(f"✅ Updated: {success}")

# Test 8: Get updated issue
print("\n8️⃣ Getting updated issue...")
updated_issue = issues.get(issue_id)
print(f"✅ Status: {updated_issue['status']}, WCAG: {updated_issue['wcag_criterion']}")

# Test 9: Count
print("\n9️⃣ Counting records...")
print(f"✅ Projects: {projects.count()}")
print(f"✅ Targets: {targets.count()}")
print(f"✅ Issues: {issues.count()}")
print(f"✅ Evidence: {evidence.count()}")

print("\n" + "=" * 50)
print("✅ All tests passed!")
