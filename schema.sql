-- A11y Workbench Database Schema
-- Version: 1.0
-- Date: 2026-03-06

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    client_name TEXT,
    description TEXT,
    tags TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_created ON projects(created_at);

-- Targets
CREATE TABLE IF NOT EXISTS targets (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    flow_type TEXT DEFAULT 'page',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_targets_project ON targets(project_id);
CREATE INDEX IF NOT EXISTS idx_targets_flow_type ON targets(flow_type);

-- Test Sessions
CREATE TABLE IF NOT EXISTS test_sessions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    assistive_tech TEXT NOT NULL,
    browser TEXT NOT NULL,
    platform TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    tester_notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_project ON test_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_target ON test_sessions(target_id);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON test_sessions(started_at);

-- Finding Groups
CREATE TABLE IF NOT EXISTS finding_groups (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    target_id TEXT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_finding_groups_project ON finding_groups(project_id);
CREATE INDEX IF NOT EXISTS idx_finding_groups_target ON finding_groups(target_id);
CREATE INDEX IF NOT EXISTS idx_finding_groups_category ON finding_groups(category);

-- Issues
CREATE TABLE IF NOT EXISTS issues (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    target_id TEXT,
    session_id TEXT,
    finding_group_id TEXT,
    title TEXT NOT NULL,
    raw_note TEXT,
    description TEXT,
    steps_to_reproduce TEXT,
    observed_behavior TEXT,
    expected_behavior TEXT,
    user_impact TEXT,
    severity TEXT NOT NULL,
    confidence TEXT NOT NULL DEFAULT 'exact',
    affected_element TEXT,
    wcag_criterion TEXT,
    suggested_fix TEXT,
    tags TEXT,
    source_type TEXT NOT NULL DEFAULT 'manual',
    status TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE SET NULL,
    FOREIGN KEY (session_id) REFERENCES test_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (finding_group_id) REFERENCES finding_groups(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_issues_project ON issues(project_id);
CREATE INDEX IF NOT EXISTS idx_issues_target ON issues(target_id);
CREATE INDEX IF NOT EXISTS idx_issues_session ON issues(session_id);
CREATE INDEX IF NOT EXISTS idx_issues_group ON issues(finding_group_id);
CREATE INDEX IF NOT EXISTS idx_issues_severity ON issues(severity);
CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
CREATE INDEX IF NOT EXISTS idx_issues_wcag ON issues(wcag_criterion);
CREATE INDEX IF NOT EXISTS idx_issues_source ON issues(source_type);

-- Evidence
CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    issue_id TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_evidence_issue ON evidence(issue_id);
CREATE INDEX IF NOT EXISTS idx_evidence_type ON evidence(type);

-- Checklists
CREATE TABLE IF NOT EXISTS checklists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    items TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_checklists_category ON checklists(category);

-- Checklist Results
CREATE TABLE IF NOT EXISTS checklist_results (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    checklist_id TEXT NOT NULL,
    item_key TEXT NOT NULL,
    item_label TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES test_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_checklist_results_session ON checklist_results(session_id);
CREATE INDEX IF NOT EXISTS idx_checklist_results_checklist ON checklist_results(checklist_id);
CREATE INDEX IF NOT EXISTS idx_checklist_results_status ON checklist_results(status);

-- Templates
CREATE TABLE IF NOT EXISTS templates (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    default_title TEXT NOT NULL,
    description_skeleton TEXT,
    typical_impact TEXT,
    likely_wcag TEXT,
    suggested_fix_skeleton TEXT,
    suggested_tags TEXT,
    typical_evidence_type TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_templates_category ON templates(category);

-- Exports
CREATE TABLE IF NOT EXISTS exports (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    export_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_exports_project ON exports(project_id);
CREATE INDEX IF NOT EXISTS idx_exports_type ON exports(export_type);
CREATE INDEX IF NOT EXISTS idx_exports_created ON exports(created_at);
