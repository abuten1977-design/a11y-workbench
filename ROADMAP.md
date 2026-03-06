# 🗺️ ROADMAP: A11y Workbench

**Версія:** 2.0  
**Дата:** 6 березня 2026  
**Статус:** Phase 1 - Документація та архітектура

---

## 🎯 НОВА МЕТА

**A11y Workbench** - персональна виробнича система незрячого accessibility-експерта

**НЕ marketplace, НЕ платформа для багатьох користувачів**

**Це інструмент, який допомагає:**
- Швидко фіксувати проблеми доступності
- Перетворювати нотатки в професійні звіти
- Зберігати проектну історію
- Експортувати звіти для клієнтів
- Збирати портфоліо
- Отримати роботу в Данії / international remote

---

## 📊 АРХІТЕКТУРА

### Було (v0.3.0):
```
Job Queue System
├── /api/v1/check - створити завдання
├── /api/v1/queue - черга
├── /dashboard - взяти завдання
└── Alt+1/2/3/0 - оцінка
```

### Стає (v1.0):
```
Project-Based Workflow
├── Projects (клієнти)
│   └── Targets (сторінки/flows)
│       └── TestSessions (сесії тестування)
│           └── FindingGroups (групи проблем)
│               └── Issues (дефекти)
│                   └── Evidence (докази)
├── Checklists (структуроване тестування)
├── Templates (типові проблеми)
├── Exports (Markdown/JSON/CSV)
├── Statistics (портфоліо метрики)
└── AI Assistant (note → structured report)
```

---

## 🏗️ PHASES

### ✅ PHASE 0: Prototype (ЗАВЕРШЕНО)
**Термін:** Лютий-березень 2026  
**Статус:** ✅ Готово

**Що зроблено:**
- FastAPI backend
- Dashboard з hotkeys
- Черга завдань
- Детальна форма звіту
- WCAG 2.2 база (87 критеріїв)
- Google Cloud deployment
- Systemd service

**Результат:** Робочий прототип, але модель "job queue", не "project workflow"

---

### 🔄 PHASE 1: REFRAME + DATA CORE (В ПРОЦЕСІ)
**Термін:** 3-5 днів  
**Статус:** 🔄 В процесі

**Завдання:**
- [x] Оновити документацію (ROADMAP, BIG_PICTURE)
- [ ] Створити ARCHITECTURE.md
- [ ] Створити DATA_MODEL.md
- [ ] Створити SERVICES.md
- [ ] Створити CAREER_STRATEGY.md
- [ ] Міграція з JSON → SQLite
- [ ] Нова схема бази (Project/Target/Session/FindingGroup/Issue/Evidence)
- [ ] Міграційний скрипт для старих даних
- [ ] Прибрати "$5 за тест"

**Результат:**
- Оновлена документація
- SQLite база з новими таблицями
- Збережена сумісність з існуючими даними

---

### ⏳ PHASE 2: ISSUE WORKFLOW
**Термін:** 10-14 днів  
**Статус:** ⏳ Чекає

**Завдання:**
- [ ] Projects CRUD
- [ ] Targets/Flows CRUD
- [ ] Test Sessions
- [ ] FindingGroups (організація issues)
- [ ] Issues з повною структурою + tags
- [ ] Evidence (screen reader output, код)
- [ ] Статуси життєвого циклу
- [ ] Quick Capture (швидкий ввід)
- [ ] Structured Report (повна форма)
- [ ] Фільтри по tags, severity, status

**Два режими:**

**Quick Capture:**
```
"submit button unlabeled in checkout"
→ Зберігається як raw_note
→ Можна доповнити пізніше
```

**Structured Report:**
```
- Title
- Steps to reproduce
- Observed behavior
- Expected behavior
- User impact
- Severity
- WCAG criterion
- Suggested fix
- Evidence
- Tags
```

**Результат:**
- Dashboard з проектами
- Створення issues з evidence
- Фільтри та пошук
- Retest queue

---

### ⏳ PHASE 2.5: CHECKLIST SYSTEM
**Термін:** 3-5 днів  
**Статус:** ⏳ Чекає

**Завдання:**
- [ ] Базові чеклісти (Navigation, Forms, Buttons, ARIA, Focus, Semantics)
- [ ] UI для роботи з чеклістами
- [ ] Відмітки: pass / fail / not applicable
- [ ] Автоматичне створення issues з failed items
- [ ] Збереження результатів

**Чеклісти:**
- Navigation (skip link, headings, landmarks)
- Forms (labels, errors, focus order)
- Buttons (accessible name, keyboard)
- ARIA (roles, states, properties)
- Focus (visible, logical, no traps)
- Semantics (proper HTML, hierarchy)

**Результат:**
- Бібліотека чеклістів
- Швидке структуроване тестування
- Автогенерація issues

---

### ⏳ PHASE 3: EXPORTS + PORTFOLIO
**Термін:** 7 днів  
**Статус:** ⏳ Чекає

**Завдання:**
- [ ] Markdown export (developer report)
- [ ] JSON/CSV export
- [ ] Client summary з statistics
- [ ] Developer issue list з evidence
- [ ] Portfolio mode (anonymize)
- [ ] Sample reports
- [ ] Statistics dashboard

**Експорти:**

**MVP (обов'язково):**
- ✅ Markdown
- ✅ JSON
- ✅ CSV

**Пізніше (опціонально):**
- ⏳ DOCX

**Statistics:**
- Projects tested
- Issues found (by severity)
- WCAG criteria referenced in findings
- Most common issue types
- Evidence collected
- Issue sources (manual/checklist/AI)

**Результат:**
- 3 формати експорту
- Sample reports для портфоліо
- Statistics для CV

---

### ⏳ PHASE 4: AI ASSISTANT
**Термін:** 5 днів  
**Статус:** ⏳ Чекає

**Завдання:**
- [ ] Defect template library (20 шаблонів)
- [ ] AI endpoint (3 функції!)
- [ ] Safe prompting strategy
- [ ] Integration в UI

**AI функції (ТІЛЬКИ 3!):**

**1. Raw note → Structured draft**
```
Вхід: "submit button unlabeled, NVDA says button only"
Вихід: Title, Steps, Observed, Expected, Impact, WCAG, Fix
```

**2. Suggest template**
- Розпізнати тип проблеми
- Запропонувати шаблон

**3. Suggest WCAG**
- На основі опису
- З confidence level: "Probable WCAG: 4.1.2 (80%)"

**НЕ робимо:**
- ❌ Report validation
- ❌ Complex remediation
- ❌ Вигадування фактів

**Результат:**
- Швидке перетворення нотаток
- Бібліотека шаблонів
- AI без overengineering

---

### ⏳ PHASE 5: HARDENING
**Термін:** 1-2 тижні  
**Статус:** ⏳ Чекає

**Завдання:**
- [ ] Basic auth
- [ ] HTTPS (Let's Encrypt)
- [ ] .env strategy
- [ ] Backup strategy для SQLite
- [ ] CLI для backup/restore
- [ ] Rate limiting
- [ ] Debug exposure check
- [ ] Deployment improvements

**Результат:**
- Безпечна система
- Автоматичні backup
- Production-ready

---

## 📅 TIMELINE

```
Week 1:  Phase 1 (docs + SQLite)
Week 2:  Phase 2 (project workflow)
Week 3:  Phase 2.5 + Phase 3 (checklists + exports)
Week 4:  Phase 4 + Phase 5 (AI + hardening)
```

**Загальний час:** 3-4 тижні

---

## 🎯 КІНЦЕВИЙ РЕЗУЛЬТАТ

**Після завершення я зможу:**
1. ✅ Створити проект для клієнта
2. ✅ Додати URL/flows
3. ✅ Почати тестову сесію
4. ✅ Швидко фіксувати баги (Quick Capture)
5. ✅ Довести до професійного вигляду
6. ✅ Експортувати developer-ready report
7. ✅ Експортувати client summary
8. ✅ Зберегти sample report в портфоліо
9. ✅ Показати систему роботодавцю
10. ✅ Брати платні замовлення

---

## 🚫 ЩО НЕ РОБИМО

**Щоб не зірватись в overengineering:**
- ❌ Multi-user system
- ❌ Billing/payments
- ❌ RBAC
- ❌ Jira integration
- ❌ Складна AI
- ❌ "Ідеальна" аналітика
- ❌ DOCX для MVP

**Фокус:** Personal production tool, не SaaS platform

---

## 📊 МЕТРИКИ УСПІХУ

**Технічні:**
- SQLite замість JSON
- 7 основних сутностей
- 3 формати експорту
- 20 defect templates
- 6 базових чеклістів

**Бізнесові:**
- Готовий sample report
- Statistics для CV
- Proof of workflow
- Можливість брати замовлення

---

## 🔗 ЗВ'ЯЗАНІ ДОКУМЕНТИ

- `EXECUTION_PLAN.md` - детальний план виконання
- `BIG_PICTURE.md` - загальна картина проекту
- `ARCHITECTURE.md` - технічна архітектура
- `DATA_MODEL.md` - схема бази даних
- `SERVICES.md` - продаваємі послуги
- `CAREER_STRATEGY.md` - кар'єрна стратегія
- `PROJECT_STATUS.md` - поточний статус

---

**Останнє оновлення:** 6 березня 2026, 18:10 CET  
**Версія:** 2.0 (A11y Workbench)
