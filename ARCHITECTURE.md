# 🏗️ ARCHITECTURE: A11y Workbench

**Версія:** 1.0  
**Дата:** 6 березня 2026

---

## 🎯 АРХІТЕКТУРНІ ПРИНЦИПИ

1. **Simplicity** - просто, не складно
2. **Reliability** - надійність > краса
3. **Accessibility** - NVDA-friendly обов'язково
4. **No overengineering** - мінімум для роботи
5. **Single user** - не багатокористувацька система

---

## 📊 HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────┐
│           User (Blind Tester)               │
│         Windows + NVDA + Browser            │
└──────────────────┬──────────────────────────┘
                   │ HTTP/HTTPS
                   ↓
┌─────────────────────────────────────────────┐
│         Google Cloud (e2-micro)             │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │       FastAPI Application             │ │
│  │                                       │ │
│  │  ┌─────────────┐  ┌────────────────┐ │ │
│  │  │  Dashboard  │  │   API Routes   │ │ │
│  │  │   (HTML)    │  │   (REST)       │ │ │
│  │  └─────────────┘  └────────────────┘ │ │
│  │                                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │      Business Logic             │ │ │
│  │  │  - Projects                     │ │ │
│  │  │  - Issues                       │ │ │
│  │  │  - Checklists                   │ │ │
│  │  │  - Exports                      │ │ │
│  │  │  - AI Assistant                 │ │ │
│  │  └─────────────────────────────────┘ │ │
│  │                                       │ │
│  │  ┌─────────────────────────────────┐ │ │
│  │  │      Data Layer                 │ │ │
│  │  │  - SQLite                       │ │ │
│  │  │  - Repository Pattern           │ │ │
│  │  └─────────────────────────────────┘ │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │         SQLite Database               │ │
│  │  /home/butenhome/a11y-api/data.db     │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │         Static Files                  │ │
│  │  - WCAG JSON                          │ │
│  │  - Templates                          │ │
│  │  - Checklists                         │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 🗄️ DATA ARCHITECTURE

### Storage Strategy

**SQLite Database:**
- Локація: `/home/butenhome/a11y-api/data.db`
- Backup: щоденний автоматичний backup
- Міграції: Alembic або ручні SQL скрипти

**Static Files:**
- WCAG JSON: `/home/butenhome/a11y-api/wcag_criteria_simple.json`
- Templates: `/home/butenhome/a11y-api/templates/`
- Checklists: `/home/butenhome/a11y-api/checklists/`

**Exports:**
- Локація: `/home/butenhome/a11y-api/exports/`
- Формати: Markdown, JSON, CSV
- Cleanup: старі файли видаляються через 30 днів

---

### Entity Relationships

```
Project (1) ──────< (N) Target
                         │
                         └──< (N) TestSession
                                   │
                                   ├──< (N) FindingGroup
                                   │         │
                                   │         └──< (N) Issue
                                   │                   │
                                   │                   └──< (N) Evidence
                                   │
                                   └──< (N) ChecklistResult

Checklist (1) ──────< (N) ChecklistResult

Template (1) ──────< (N) Issue (suggested_template_id)
```

---

## 🔌 API ARCHITECTURE

### REST API Endpoints

**Projects:**
```
GET    /api/v1/projects              - List projects
POST   /api/v1/projects              - Create project
GET    /api/v1/projects/{id}         - Get project
PUT    /api/v1/projects/{id}         - Update project
DELETE /api/v1/projects/{id}         - Delete project
```

**Targets:**
```
GET    /api/v1/projects/{id}/targets       - List targets
POST   /api/v1/projects/{id}/targets       - Create target
GET    /api/v1/targets/{id}                - Get target
PUT    /api/v1/targets/{id}                - Update target
DELETE /api/v1/targets/{id}                - Delete target
```

**Test Sessions:**
```
GET    /api/v1/targets/{id}/sessions       - List sessions
POST   /api/v1/targets/{id}/sessions       - Create session
GET    /api/v1/sessions/{id}               - Get session
PUT    /api/v1/sessions/{id}               - Update session
DELETE /api/v1/sessions/{id}               - Delete session
```

**Issues:**
```
GET    /api/v1/projects/{id}/issues        - List issues
POST   /api/v1/issues                      - Create issue (Quick Capture)
POST   /api/v1/issues/structured           - Create issue (Structured)
GET    /api/v1/issues/{id}                 - Get issue
PUT    /api/v1/issues/{id}                 - Update issue
DELETE /api/v1/issues/{id}                 - Delete issue
GET    /api/v1/issues?tags=keyboard        - Filter by tags
GET    /api/v1/issues?severity=critical    - Filter by severity
```

**Evidence:**
```
POST   /api/v1/issues/{id}/evidence        - Add evidence
GET    /api/v1/evidence/{id}               - Get evidence
DELETE /api/v1/evidence/{id}               - Delete evidence
```

**Checklists:**
```
GET    /api/v1/checklists                  - List checklists
POST   /api/v1/sessions/{id}/checklist     - Start checklist
PUT    /api/v1/checklist-results/{id}      - Update result
```

**Exports:**
```
POST   /api/v1/projects/{id}/export        - Export project
GET    /api/v1/exports/{id}                - Download export
```

**AI Assistant:**
```
POST   /api/v1/ai/polish                   - Polish raw note
POST   /api/v1/ai/suggest-template         - Suggest template
POST   /api/v1/ai/suggest-wcag             - Suggest WCAG
```

**Statistics:**
```
GET    /api/v1/stats                       - Overall statistics
GET    /api/v1/projects/{id}/stats         - Project statistics
```

**Legacy (compatibility):**
```
GET    /api/v1/wcag                        - Get WCAG criteria
GET    /health                             - Health check
```

---

## 🖥️ FRONTEND ARCHITECTURE

### Dashboard Structure

```
/dashboard
├── /projects                    - Projects list
├── /projects/{id}               - Project details
│   ├── /targets                 - Targets list
│   ├── /sessions                - Sessions list
│   └── /issues                  - Issues list
├── /sessions/{id}               - Test session
│   ├── /quick-capture           - Quick capture form
│   ├── /checklist               - Checklist UI
│   └── /issues                  - Issues for session
├── /issues/{id}                 - Issue detail/edit
│   └── /evidence                - Evidence list
├── /exports                     - Export center
└── /stats                       - Statistics dashboard
```

### UI Components

**Accessibility Requirements:**
- Keyboard navigation (Tab, Arrow keys)
- NVDA screen reader support
- Logical heading structure (h1 → h2 → h3)
- ARIA landmarks (header, nav, main, footer)
- Focus management
- No keyboard traps
- Hotkeys as enhancement (not sole mechanism)

**Key Components:**
- ProjectList
- ProjectDetail
- TargetList
- SessionView
- QuickCaptureForm
- StructuredReportForm
- ChecklistUI
- IssueList (with filters)
- IssueDetail
- EvidenceCapture
- ExportCenter
- StatsDashboard

---

## 🧠 AI ARCHITECTURE

### AI Assistant Design

**Provider:** OpenAI API або Claude API (вибрати пізніше)

**Functions (ТІЛЬКИ 3!):**

**1. Polish Raw Note**
```python
def polish_note(raw_note: str) -> StructuredIssue:
    """
    Перетворює короткий нотаток у структурований звіт
    
    Input: "submit button unlabeled, NVDA says button only"
    Output: {
        "title": "Unlabeled Submit Button",
        "steps": "Navigate to form, tab to submit button",
        "observed": "NVDA announces 'button' without label",
        "expected": "Should announce button purpose",
        "impact": "Users cannot identify button function",
        "wcag": "4.1.2",
        "confidence": 0.9,
        "tags": ["button", "screen-reader", "forms"]
    }
    """
```

**2. Suggest Template**
```python
def suggest_template(raw_note: str) -> Template:
    """
    Розпізнає тип проблеми та пропонує шаблон
    
    Input: "button has no label"
    Output: Template("unlabeled_button")
    """
```

**3. Suggest WCAG**
```python
def suggest_wcag(description: str) -> WCAGSuggestion:
    """
    Пропонує WCAG критерій з confidence level
    
    Input: "Button not accessible with keyboard"
    Output: {
        "criterion": "2.1.1",
        "title": "Keyboard",
        "level": "A",
        "confidence": 0.85
    }
    """
```

**Prompting Strategy:**
- System prompt з WCAG knowledge
- Few-shot examples
- Uncertainty labels обов'язкові
- Не вигадувати факти
- Режим "structure only"

**Caching:**
- Кешувати WCAG mappings
- Кешувати template suggestions
- Зменшити API calls

---

## 🔒 SECURITY ARCHITECTURE

### Authentication

**Phase 1 (MVP):**
- Basic Auth (username/password)
- Single user
- Environment variables для credentials

**Phase 5 (Hardening):**
- HTTPS (Let's Encrypt)
- Session management
- CSRF protection
- Rate limiting

### Data Protection

**Sensitive Data:**
- Client names (можна anonymize для portfolio)
- URLs (можна приховати для demo)
- Evidence (screen reader output - не sensitive)

**Backup Strategy:**
- Щоденний backup SQLite
- Зберігати 7 днів
- Можливість restore

**Environment Variables:**
```
A11Y_DB_PATH=/home/butenhome/a11y-api/data.db
A11Y_BACKUP_PATH=/home/butenhome/a11y-api/backups/
A11Y_EXPORT_PATH=/home/butenhome/a11y-api/exports/
A11Y_AUTH_USER=admin
A11Y_AUTH_PASSWORD=<secure_password>
OPENAI_API_KEY=<api_key>
```

---

## 📦 DEPLOYMENT ARCHITECTURE

### Current Setup

**Server:**
- Google Cloud Compute Engine
- e2-micro (Free Tier)
- Ubuntu 20.04
- IP: 34.58.51.76

**Application:**
- FastAPI + Uvicorn
- Systemd service: `a11y-api.service`
- Working directory: `/home/butenhome/a11y-api/`
- Python venv: `/home/butenhome/a11y-api/venv/`

**Deployment Process:**
```bash
# 1. Copy files to server
gcloud compute scp api_server.py a11y-server:/tmp/ --zone=us-central1-a

# 2. Move to working directory
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo cp /tmp/api_server.py /home/butenhome/a11y-api/ &&
    sudo chown butenhome:butenhome /home/butenhome/a11y-api/api_server.py
"

# 3. Restart service
gcloud compute ssh a11y-server --zone=us-central1-a --command="
    sudo systemctl restart a11y-api
"
```

**Systemd Service:**
```ini
[Unit]
Description=A11y Workbench API Server
After=network.target

[Service]
Type=simple
User=butenhome
WorkingDirectory=/home/butenhome/a11y-api
ExecStart=/home/butenhome/a11y-api/venv/bin/uvicorn api_server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🧪 TESTING STRATEGY

### Manual Testing

**Primary:**
- NVDA screen reader testing
- Keyboard navigation testing
- Real-world workflow testing

**Tools:**
- NVDA (primary)
- Chrome DevTools
- curl для API testing

### Automated Testing (опціонально пізніше)

**Unit Tests:**
- Business logic
- Data layer
- AI prompting

**Integration Tests:**
- API endpoints
- Database operations

**NOT doing:**
- ❌ E2E testing (занадто складно)
- ❌ Load testing (single user)
- ❌ Security testing (basic auth достатньо)

---

## 📊 MONITORING & LOGGING

### Logging

**Levels:**
- ERROR - критичні помилки
- WARNING - потенційні проблеми
- INFO - важливі події
- DEBUG - детальна інформація (тільки для розробки)

**Log Files:**
- Application: `journalctl -u a11y-api`
- SQLite: query logging (опціонально)

### Monitoring

**Basic:**
- Systemd status
- Disk space
- Database size

**NOT doing:**
- ❌ Prometheus/Grafana (overengineering)
- ❌ APM tools (не потрібно)
- ❌ Alerting (single user)

---

## 🔄 MIGRATION STRATEGY

### From v0.3.0 to v1.0

**Data Migration:**
1. Читати старі JSON файли (`/tmp/a11y_queue.json`, `/tmp/a11y_results.json`)
2. Конвертувати в нову структуру (Project → Target → Issue)
3. Зберегти в SQLite
4. Backup старих JSON
5. Видалити старі JSON (після підтвердження)

**Code Migration:**
- Зберегти старі endpoints для compatibility
- Додати нові endpoints поступово
- Deprecate старі endpoints через 1 місяць

**Dashboard Migration:**
- Нова версія на `/dashboard`
- Стара версія на `/dashboard/legacy` (тимчасово)
- Redirect через 2 тижні

---

## 🚫 ANTI-PATTERNS (ЩО НЕ РОБИМО)

1. **Microservices** - занадто складно для single user
2. **GraphQL** - REST достатньо
3. **Redis/Memcached** - SQLite достатньо швидкий
4. **Docker/Kubernetes** - overengineering
5. **Complex ORM** - прості SQL queries достатньо
6. **Frontend framework** - Vanilla JS достатньо
7. **WebSockets** - polling достатньо
8. **Message queues** - не потрібно
9. **CDN** - не потрібно
10. **Load balancer** - single server достатньо

---

## 📚 TECHNOLOGY STACK

**Backend:**
- Python 3.10+
- FastAPI
- Uvicorn
- SQLite3
- Pydantic

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript
- Fetch API

**Infrastructure:**
- Google Cloud Compute Engine
- Systemd
- Git

**AI:**
- OpenAI API або Claude API (TBD)

**Tools:**
- Git
- gcloud CLI
- curl
- NVDA

---

## 🔮 FUTURE CONSIDERATIONS

**Якщо проект виросте:**
- PostgreSQL замість SQLite
- HTTPS обов'язково
- Proper authentication
- API rate limiting
- Webhook support
- Multi-user (можливо)

**Але це НЕ зараз!**

---

**Останнє оновлення:** 6 березня 2026, 18:20 CET  
**Версія:** 1.0  
**Статус:** Phase 1 - Documentation
