#!/usr/bin/env python3
"""
Parse axe-core results and format for A11y Workbench
"""

import json
import sys
from pathlib import Path

def parse_axe_results(json_file: str):
    """Parse axe JSON results into readable format"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    violations = data.get('violations', [])
    url = data.get('url', 'Unknown')
    
    print(f"\n{'='*80}")
    print(f"AXE-CORE RESULTS: {url}")
    print(f"{'='*80}\n")
    
    print(f"📊 Summary:")
    print(f"   Total violations: {len(violations)}")
    print(f"   Total passes: {len(data.get('passes', []))}")
    print(f"   Incomplete: {len(data.get('incomplete', []))}")
    print(f"\n{'='*80}\n")
    
    if not violations:
        print("✅ No violations found!\n")
        return
    
    # Group by impact
    by_impact = {'critical': [], 'serious': [], 'moderate': [], 'minor': []}
    for v in violations:
        impact = v.get('impact', 'moderate')
        by_impact[impact].append(v)
    
    # Print by severity
    for impact in ['critical', 'serious', 'moderate', 'minor']:
        issues = by_impact[impact]
        if not issues:
            continue
            
        print(f"\n{'#'*80}")
        print(f"# {impact.upper()} ({len(issues)} issues)")
        print(f"{'#'*80}\n")
        
        for idx, issue in enumerate(issues, 1):
            print(f"\n{idx}. {issue['help']}")
            print(f"   ID: {issue['id']}")
            print(f"   Impact: {issue['impact']}")
            print(f"   WCAG: {', '.join(issue.get('tags', []))}")
            print(f"   Description: {issue['description']}")
            print(f"   Affected elements: {len(issue['nodes'])}")
            
            # Show first affected element
            if issue['nodes']:
                node = issue['nodes'][0]
                print(f"\n   Example element:")
                print(f"   HTML: {node.get('html', 'N/A')[:100]}...")
                print(f"   Target: {node.get('target', 'N/A')}")
                
                # Show failure summary
                if node.get('failureSummary'):
                    print(f"\n   Issue: {node['failureSummary'][:200]}...")
            
            print(f"\n   How to fix: {issue.get('helpUrl', 'N/A')}")
            print(f"   {'-'*76}")
    
    print(f"\n{'='*80}\n")
    
    # Export for A11y Workbench
    print("\n📋 READY FOR A11Y WORKBENCH:\n")
    print("Copy these issues to your system:\n")
    
    for impact in ['critical', 'serious', 'moderate', 'minor']:
        issues = by_impact[impact]
        for issue in issues:
            wcag_tags = [t for t in issue.get('tags', []) if 'wcag' in t.lower()]
            wcag = wcag_tags[0].replace('wcag', '').replace('a', '.').replace('aa', '') if wcag_tags else ''
            
            print(f"Title: {issue['help']}")
            print(f"Severity: {impact}")
            print(f"WCAG: {wcag}")
            print(f"Description: {issue['description']}")
            print(f"Affected: {len(issue['nodes'])} elements")
            print(f"Help: {issue.get('helpUrl', '')}")
            print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_axe.py <axe_results.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    if not Path(json_file).exists():
        print(f"Error: File {json_file} not found")
        sys.exit(1)
    
    parse_axe_results(json_file)
