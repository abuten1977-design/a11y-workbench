# 🗄️ DATA MODEL: A11y Workbench

**Версія:** 1.0  
**Дата:** 6 березня 2026

---

## 📊 DATABASE SCHEMA

### SQLite Database: `data.db`

---

## 📋 TABLES

### 1. projects

**Опис:** Клієнтські проекти

```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,  -- UUID
    name TEXT NOT NULL,
    client_name TEXT,
    description TEXT,
    tags TEXT,  -- JSON array: ["ecommerce", "forms"]
    status TEXT NOT NULL DEFAULT 'active',  -- active, completed, archived
    created_at TEXT NOT NULL,  -- ISO 8601
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created ON projects(created_at);
```

**Приклад:**
```json
{
  "id": "proj_123",
  "name": "Acme Corp Website Audit",
  "client_name": "Acme Corp",
  "description": "Full accessibility audit",
  "tags": ["ecommerce", "checkout"],
  "status": "active",
  "created_at": "2026-03-06T10:00:00Z",
  "updated_at": "2026-03-06T10:00:00Z"
}
```

---

### 2. targets

**Опис:** Сторінки/flows для тестування

```sql
CREATE TABLE targets (
    id TEXT PRIMARY KEY,  -- UUID
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    flow_type TEXT NOT NULL,  -- page, form, checkout, auth, menu, modal, search, table, other
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_targets_project ON targets(project_id);
CREATE INDEX idx_targets_flow_type ON targets(flow_type);
```

**Приклад:**
```json
{
  "id": "target_456",
  "project_id": "proj_123",
  "name": "Checkout Flow",
  "url": "https://example.com/checkout",
  "flow_type": "checkout",
  "notes": "Multi-step checkout with payment",
  "created_at": "2026-03-06T10:05:00Z",
  "updated_at": "2026-03-06T10:05:00Z"
}
```

---

### 3. test_sessions

**Опис:** Сесії тестування

```sql
CREATE TABLE test_sessions (
    id TEXT PRIMARY KEY,  -- UUID
    project_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    assistive_tech TEXT NOT NULL,  -- NVDA, VoiceOver, JAWS, TalkBack
    browser TEXT NOT NULL,  -- Chrome, Firefox, Safari, Edge
    platform TEXT NOT NULL,  -- Windows, macOS, iOS, Android
    started_at TEXT NOT NULL,
    completed_at TEXT,
    tester_notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_project ON test_sessions(project_id);
CREATE INDEX idx_sessions_target ON test_sessions(target_id);
CREATE INDEX idx_sessions_started ON test_sessions(started_at);
```

**Приклад:**
```json
{
  "id": "session_789",
  "project_id": "proj_123",
  "target_id": "target_456",
  "assistive_tech": "NVDA",
  "browser": "Chrome",
  "platform": "Windows",
  "started_at": "2026-03-06T11:00:00Z",
  "completed_at": "2026-03-06T11:30:00Z",
  "tester_notes": "Found several keyboard issues"
}
```

---

### 4. finding_groups

**Опис:** Групи знахідок (організація issues)

```sql
CREATE TABLE finding_groups (
    id TEXT PRIMARY KEY,  -- UUID
    project_id TEXT NOT NULL,
    target_id TEXT,  -- Може бути NULL якщо група для всього проекту
    name TEXT NOT NULL,
    category TEXT NOT NULL,  -- forms, navigation, buttons, aria, focus, semantics, other
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE SET NULL
);

CREATE INDEX idx_finding_groups_project ON finding_groups(project_id);
CREATE INDEX idx_finding_groups_target ON finding_groups(target_id);
CREATE INDEX idx_finding_groups_category ON finding_groups(category);
```

**Приклад:**
```json
{
  "id": "group_111",
  "project_id": "proj_123",
  "target_id": "target_456",
  "name": "Form Labels",
  "category": "forms",
  "notes": "Issues related to form field labeling",
  "created_at": "2026-03-06T11:10:00Z",
  "updated_at": "2026-03-06T11:10:00Z"
}
```

---

### 5. issues

**Опис:** Дефекти доступності

```sql
CREATE TABLE issues (
    id TEXT PRIMARY KEY,  -- UUID
    project_id TEXT NOT NULL,
    target_id TEXT,
    session_id TEXT,
    finding_group_id TEXT,
    
    -- Content
    title TEXT NOT NULL,
    raw_note TEXT,  -- Оригінальний короткий нотаток
    description TEXT,
    steps_to_reproduce TEXT,
    observed_behavior TEXT,
    expected_behavior TEXT,
    user_impact TEXT,
    
    -- Classification
    severity TEXT NOT NULL,  -- minor, moderate, serious, critical
    confidence TEXT NOT NULL DEFAULT 'exact',  -- exact, probable, needs_review
    affected_element TEXT,
    wcag_criterion TEXT,  -- e.g., "1.3.1", "4.1.2"
    suggested_fix TEXT,
    tags TEXT,  -- JSON array: ["keyboard", "screen-reader", "forms"]
    source_type TEXT NOT NULL DEFAULT 'manual',  -- manual, checklist, ai_draft, imported
    
    -- Lifecycle
    status TEXT NOT NULL DEFAULT 'new',  -- new, confirmed, reported, fixed_pending_retest, retest_passed, retest_failed
    
    -- Timestamps
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE SET NULL,
    FOREIGN KEY (session_id) REFERENCES test_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (finding_group_id) REFERENCES finding_groups(id) ON DELETE SET NULL
);

CREATE INDEX idx_issues_project ON issues(project_id);
CREATE INDEX idx_issues_target ON issues(target_id);
CREATE INDEX idx_issues_session ON issues(session_id);
CREATE INDEX idx_issues_group ON issues(finding_group_id);
CREATE INDEX idx_issues_severity ON issues(severity);
CREATE INDEX idx_issues_status ON issues(status);
CREATE INDEX idx_issues_wcag ON issues(wcag_criterion);
CREATE INDEX idx_issues_source ON issues(source_type);
```

**Приклад:**
```json
{
  "id": "issue_222",
  "project_id": "proj_123",
  "target_id": "target_456",
  "session_id": "session_789",
  "finding_group_id": "group_111",
  "title": "Unlabeled Submit Button in Checkout",
  "raw_note": "submit button unlabeled, NVDA says button only",
  "description": "The submit button in the checkout form lacks an accessible name",
  "steps_to_reproduce": "1. Navigate to checkout\n2. Tab to submit button\n3. Listen to NVDA announcement",
  "observed_behavior": "NVDA announces 'button' without any label",
  "expected_behavior": "NVDA should announce 'Submit order, button' or similar",
  "user_impact": "Blind users cannot identify the button's purpose",
  "severity": "serious",
  "confidence": "exact",
  "affected_element": ".checkout-form button[type=submit]",
  "wcag_criterion": "4.1.2",
  "suggested_fix": "Add aria-label='Submit order' or visible text",
  "tags": "[\"button\", \"screen-reader\", \"forms\"]",
  "source_type": "manual",
  "status": "new",
  "created_at": "2026-03-06T11:15:00Z",
  "updated_at": "2026-03-06T11:15:00Z"
}
```

---

### 6. evidence

**Опис:** Докази для issues

```sql
CREATE TABLE evidence (
    id TEXT PRIMARY KEY,  -- UUID
    issue_id TEXT NOT NULL,
    type TEXT NOT NULL,  -- note, code, screenshot, aria_dump, screen_reader_output
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
);

CREATE INDEX idx_evidence_issue ON evidence(issue_id);
CREATE INDEX idx_evidence_type ON evidence(type);
```

**Приклад:**
```json
{
  "id": "evidence_333",
  "issue_id": "issue_222",
  "type": "screen_reader_output",
  "content": "NVDA: button",
  "created_at": "2026-03-06T11:16:00Z"
}
```

---

### 7. checklists

**Опис:** Шаблони чеклістів

```sql
CREATE TABLE checklists (
    id TEXT PRIMARY KEY,  -- UUID
    name TEXT NOT NULL,
    category TEXT NOT NULL,  -- navigation, forms, buttons, aria, focus, semantics
    items TEXT NOT NULL,  -- JSON array: [{"key": "...", "label": "..."}, ...]
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_checklists_category ON checklists(category);
```

**Приклад:**
```json
{
  "id": "checklist_forms",
  "name": "Forms Checklist",
  "category": "forms",
  "items": "[{\"key\": \"form_label_association\", \"label\": \"All inputs have associated labels\"}, {\"key\": \"error_identification\", \"label\": \"Error identification clear\"}]",
  "created_at": "2026-03-06T10:00:00Z",
  "updated_at": "2026-03-06T10:00:00Z"
}
```

---

### 8. checklist_results

**Опис:** Результати чеклістів

```sql
CREATE TABLE checklist_results (
    id TEXT PRIMARY KEY,  -- UUID
    session_id TEXT NOT NULL,
    checklist_id TEXT NOT NULL,
    item_key TEXT NOT NULL,
    item_label TEXT NOT NULL,
    status TEXT NOT NULL,  -- pass, fail, not_applicable
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES test_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);

CREATE INDEX idx_checklist_results_session ON checklist_results(session_id);
CREATE INDEX idx_checklist_results_checklist ON checklist_results(checklist_id);
CREATE INDEX idx_checklist_results_status ON checklist_results(status);
```

**Приклад:**
```json
{
  "id": "result_444",
  "session_id": "session_789",
  "checklist_id": "checklist_forms",
  "item_key": "form_label_association",
  "item_label": "All inputs have associated labels",
  "status": "fail",
  "notes": "Submit button missing label",
  "created_at": "2026-03-06T11:12:00Z"
}
```

---

### 9. templates

**Опис:** Шаблони типових проблем

```sql
CREATE TABLE templates (
    id TEXT PRIMARY KEY,  -- UUID
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    default_title TEXT NOT NULL,
    description_skeleton TEXT,
    typical_impact TEXT,
    likely_wcag TEXT,  -- JSON array: ["4.1.2", "1.3.1"]
    suggested_fix_skeleton TEXT,
    suggested_tags TEXT,  -- JSON array: ["button", "screen-reader"]
    typical_evidence_type TEXT,  -- screen_reader_output, code, etc.
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_templates_category ON templates(category);
```

**Приклад:**
```json
{
  "id": "template_unlabeled_button",
  "category": "buttons",
  "name": "Unlabeled Button",
  "default_title": "Unlabeled Button",
  "description_skeleton": "A button element lacks an accessible name",
  "typical_impact": "Screen reader users cannot identify button purpose",
  "likely_wcag": "[\"4.1.2\", \"2.4.4\"]",
  "suggested_fix_skeleton": "Add aria-label or visible text",
  "suggested_tags": "[\"button\", \"screen-reader\"]",
  "typical_evidence_type": "screen_reader_output",
  "created_at": "2026-03-06T10:00:00Z",
  "updated_at": "2026-03-06T10:00:00Z"
}
```

---

### 10. exports

**Опис:** Історія експортів

```sql
CREATE TABLE exports (
    id TEXT PRIMARY KEY,  -- UUID
    project_id TEXT NOT NULL,
    export_type TEXT NOT NULL,  -- markdown, json, csv, docx
    file_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE INDEX idx_exports_project ON exports(project_id);
CREATE INDEX idx_exports_type ON exports(export_type);
CREATE INDEX idx_exports_created ON exports(created_at);
```

---

## 🔗 RELATIONSHIPS

```
projects (1) ──────< (N) targets
projects (1) ──────< (N) test_sessions
projects (1) ──────< (N) finding_groups
projects (1) ──────< (N) issues
projects (1) ──────< (N) exports

targets (1) ──────< (N) test_sessions
targets (1) ──────< (N) finding_groups
targets (1) ──────< (N) issues

test_sessions (1) ──────< (N) issues
test_sessions (1) ──────< (N) checklist_results

finding_groups (1) ──────< (N) issues

issues (1) ──────< (N) evidence

checklists (1) ──────< (N) checklist_results

templates (1) ──────< (N) issues (suggested_template_id - опціонально)
```

---

## 📊 ENUMS

### project.status
- `active` - активний проект
- `completed` - завершений
- `archived` - архівований

### target.flow_type
- `page` - звичайна сторінка
- `form` - форма
- `checkout` - процес оформлення замовлення
- `auth` - автентифікація (login/signup)
- `menu` - навігаційне меню
- `modal` - модальне вікно
- `search` - пошук
- `table` - таблиця даних
- `other` - інше

### test_session.assistive_tech
- `NVDA`
- `VoiceOver`
- `JAWS`
- `TalkBack`
- `Narrator`
- `Other`

### test_session.browser
- `Chrome`
- `Firefox`
- `Safari`
- `Edge`
- `Other`

### test_session.platform
- `Windows`
- `macOS`
- `iOS`
- `Android`
- `Linux`

### finding_group.category
- `forms` - форми
- `navigation` - навігація
- `buttons` - кнопки
- `aria` - ARIA
- `focus` - фокус
- `semantics` - семантика
- `other` - інше

### issue.severity
- `minor` - незначна
- `moderate` - помірна
- `serious` - серйозна
- `critical` - критична

### issue.confidence
- `exact` - точно
- `probable` - ймовірно
- `needs_review` - потребує перевірки

### issue.source_type
- `manual` - ручне введення
- `checklist` - з чеклісту
- `ai_draft` - AI-згенерований чернетка
- `imported` - імпортований

### issue.status
- `new` - новий
- `confirmed` - підтверджений
- `reported` - відправлений клієнту
- `fixed_pending_retest` - виправлено, чекає перевірки
- `retest_passed` - перевірка пройдена
- `retest_failed` - перевірка не пройдена

### evidence.type
- `note` - текстовий нотаток
- `code` - фрагмент коду
- `screenshot` - скріншот (URL або base64)
- `aria_dump` - ARIA дерево
- `screen_reader_output` - вивід screen reader

### checklist_result.status
- `pass` - пройдено
- `fail` - не пройдено
- `not_applicable` - не застосовується

### export.export_type
- `markdown`
- `json`
- `csv`
- `docx` (опціонально)

---

## 🔄 MIGRATION FROM v0.3.0

### Старі дані (JSON):

**`/tmp/a11y_queue.json`:**
```json
[
  {
    "job_id": "uuid",
    "url": "https://example.com",
    "priority": 1,
    "created_at": "2026-03-05T10:00:00Z",
    "status": "pending"
  }
]
```

**`/tmp/a11y_results.json`:**
```json
{
  "uuid": {
    "job_id": "uuid",
    "url": "https://example.com",
    "rating": "issues",
    "description": "Button unlabeled",
    "element": ".submit-btn",
    "wcag_criterion": "4.1.2",
    "completed_at": "2026-03-05T10:30:00Z"
  }
}
```

### Міграційна логіка:

```python
# Псевдокод
for result in old_results:
    # Створити project
    project = create_project(
        name=f"Legacy: {result['url']}",
        status='completed'
    )
    
    # Створити target
    target = create_target(
        project_id=project.id,
        url=result['url'],
        flow_type='page'
    )
    
    # Створити issue
    issue = create_issue(
        project_id=project.id,
        target_id=target.id,
        title=result.get('description', 'Legacy issue'),
        raw_note=result.get('description'),
        severity=rating_to_severity(result['rating']),
        affected_element=result.get('element'),
        wcag_criterion=result.get('wcag_criterion'),
        source_type='imported',
        status='completed'
    )
```

---

## 📝 NOTES

**JSON Fields:**
- Всі JSON поля зберігаються як TEXT
- Парсинг/серіалізація в application layer
- Приклад: `tags TEXT` → `'["keyboard", "forms"]'`

**UUIDs:**
- Використовуємо TEXT для UUID (не INTEGER)
- Формат: `uuid.uuid4().hex` або `str(uuid.uuid4())`

**Timestamps:**
- ISO 8601 format: `2026-03-06T10:00:00Z`
- UTC timezone
- Зберігаємо як TEXT

**Cascading Deletes:**
- `ON DELETE CASCADE` - видалити залежні записи
- `ON DELETE SET NULL` - встановити NULL

**Indexes:**
- Створені для частих запитів
- Foreign keys
- Status fields
- Timestamps

---

**Останнє оновлення:** 6 березня 2026, 18:25 CET  
**Версія:** 1.0  
**Статус:** Phase 1 - Documentation
