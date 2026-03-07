"""
Export service for generating reports
"""
from typing import Dict, List, Any
from datetime import datetime
from repositories import projects, targets, issues, evidence

def export_markdown(project_id: str) -> str:
    """Generate Markdown report for project"""
    
    # Get project
    project = projects.get(project_id)
    if not project:
        return "# Project not found"
    
    # Get all issues for project
    all_issues = issues.list_by_project(project_id)
    
    # Group by severity
    by_severity = {
        'critical': [],
        'serious': [],
        'moderate': [],
        'minor': []
    }
    
    for issue in all_issues:
        severity = issue.get('severity', 'moderate')
        if severity in by_severity:
            by_severity[severity].append(issue)
    
    # Build report
    lines = []
    lines.append(f"# Accessibility Report: {project['name']}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Project:** {project['name']}")
    if project.get('client'):
        lines.append(f"**Client:** {project['client']}")
    lines.append("")
    
    # Summary
    total = len(all_issues)
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Issues:** {total}")
    lines.append(f"- **Critical:** {len(by_severity['critical'])}")
    lines.append(f"- **Serious:** {len(by_severity['serious'])}")
    lines.append(f"- **Moderate:** {len(by_severity['moderate'])}")
    lines.append(f"- **Minor:** {len(by_severity['minor'])}")
    lines.append("")
    
    # Issues by severity
    for severity in ['critical', 'serious', 'moderate', 'minor']:
        severity_issues = by_severity[severity]
        if not severity_issues:
            continue
            
        lines.append(f"## {severity.title()} Issues ({len(severity_issues)})")
        lines.append("")
        
        for idx, issue in enumerate(severity_issues, 1):
            lines.append(f"### {idx}. {issue['title']}")
            lines.append("")
            
            if issue.get('wcag_criterion'):
                lines.append(f"**WCAG:** {issue['wcag_criterion']}")
            
            lines.append(f"**Status:** {issue.get('status', 'new')}")
            lines.append("")
            
            if issue.get('description'):
                lines.append("**Description:**")
                lines.append(issue['description'])
                lines.append("")
            
            if issue.get('steps_to_reproduce'):
                lines.append("**Steps to Reproduce:**")
                lines.append(issue['steps_to_reproduce'])
                lines.append("")
            
            if issue.get('observed_behavior'):
                lines.append("**Observed Behavior:**")
                lines.append(issue['observed_behavior'])
                lines.append("")
            
            if issue.get('expected_behavior'):
                lines.append("**Expected Behavior:**")
                lines.append(issue['expected_behavior'])
                lines.append("")
            
            if issue.get('user_impact'):
                lines.append("**User Impact:**")
                lines.append(issue['user_impact'])
                lines.append("")
            
            if issue.get('suggested_fix'):
                lines.append("**Suggested Fix:**")
                lines.append(issue['suggested_fix'])
                lines.append("")
            
            # Evidence
            issue_evidence = evidence.list_by_issue(issue['id'])
            if issue_evidence:
                lines.append("**Evidence:**")
                for ev in issue_evidence:
                    lines.append(f"- *{ev['type']}:* {ev['content']}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)


def export_json(project_id: str) -> Dict[str, Any]:
    """Generate JSON export for project"""
    
    project = projects.get(project_id)
    if not project:
        return {"error": "Project not found"}
    
    all_issues = issues.list_by_project(project_id)
    
    # Add evidence to each issue
    for issue in all_issues:
        issue['evidence'] = evidence.list_by_issue(issue['id'])
    
    return {
        "project": project,
        "issues": all_issues,
        "exported_at": datetime.now().isoformat(),
        "total_issues": len(all_issues)
    }


def export_csv(project_id: str) -> str:
    """Generate CSV export for project"""
    
    all_issues = issues.list_by_project(project_id)
    
    lines = []
    # Header
    lines.append("ID,Title,Severity,Status,WCAG,Target,Created")
    
    # Rows
    for issue in all_issues:
        row = [
            issue['id'],
            f'"{issue["title"]}"',
            issue.get('severity', ''),
            issue.get('status', ''),
            issue.get('wcag_criterion', ''),
            issue.get('target_id', ''),
            issue.get('created_at', '')
        ]
        lines.append(','.join(row))
    
    return "\n".join(lines)


def get_statistics(project_id: str = None) -> Dict[str, Any]:
    """Get statistics for project or all projects"""
    
    if project_id:
        # Project stats
        all_issues = issues.list_by_project(project_id)
        project = projects.get(project_id)
        
        stats = {
            "project_name": project['name'] if project else "Unknown",
            "total_issues": len(all_issues),
            "by_severity": {},
            "by_status": {},
            "wcag_criteria": []
        }
    else:
        # Global stats
        all_projects = projects.list_all()
        all_issues = []
        for proj in all_projects:
            all_issues.extend(issues.list_by_project(proj['id']))
        
        stats = {
            "total_projects": len(all_projects),
            "total_issues": len(all_issues),
            "by_severity": {},
            "by_status": {},
            "wcag_criteria": []
        }
    
    # Count by severity
    for issue in all_issues:
        severity = issue.get('severity', 'moderate')
        stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
    
    # Count by status
    for issue in all_issues:
        status = issue.get('status', 'new')
        stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
    
    # Collect WCAG criteria
    wcag_set = set()
    for issue in all_issues:
        if issue.get('wcag_criterion'):
            wcag_set.add(issue['wcag_criterion'])
    stats['wcag_criteria'] = sorted(list(wcag_set))
    
    return stats
