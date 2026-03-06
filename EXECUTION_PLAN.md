# 🎯 ПЛАН ВИКОНАННЯ: A11y Workbench

**Дата:** 6 березня 2026  
**Статус:** Чекає затвердження

---

## 🔴 КРИТИЧНА ЗМІНА СТРАТЕГІЇ

### БУЛО:
Платформа-маркетплейс для багатьох тестувальників з ігровою економікою ($5 за тест)

### СТАЛО:
**A11y Workbench** - персональна виробнича система незрячого accessibility-експерта

---

## 🎯 ГОЛОВНА МЕТА

**Створити production-grade систему, яка допомагає:**
1. Швидко фіксувати проблеми доступності під час ручного тестування
2. Перетворювати короткі нотатки в професійні defect reports
3. Зберігати проектну історію
4. Експортувати звіти для клієнтів та розробників
5. Збирати sample reports для портфоліо
6. Підтримувати реальну роботу з клієнтами
7. Допомогти отримати роботу в Данії / international remote

**НЕ будуємо:**
- ❌ Marketplace
- ❌ Багатокористувацьку платформу
- ❌ Складну billing-систему
- ❌ Fake economy
- ❌ Overengineering

---

## 📊 НОВА МОДЕЛЬ ДАНИХ

### Базові сутності:

**Project** (клієнт/проект):
- id, name, client_name, description, tags, status, created_at, updated_at

**Target/Page/Flow** (що тестуємо):
- id, project_id, name, url, flow_type (page/form/checkout/auth/menu/modal), notes

**TestSession** (сесія тестування):
- id, project_id, target_id, assistive_tech (NVDA/VoiceOver/JAWS), browser, platform, started_at, completed_at, tester_notes

**FindingGroup** (група знахідок) - НОВЕ!
- id, project_id, target_id, name, category (forms/navigation/buttons/aria/focus/semantics), notes
- Приклад: "Form Labels", "Button Labeling", "Error Handling", "Focus Management"

**Issue** (дефект):
- id, project_id, target_id, session_id, finding_group_id
- title, raw_note, description
- steps_to_reproduce, observed_behavior, expected_behavior
- user_impact, severity (minor/moderate/serious/critical)
- confidence (exact/probable/needs_review)
- affected_element, wcag_criterion, suggested_fix
- tags (keyboard, screen-reader, forms, navigation, modal, aria, semantics, focus)
- source_type (manual/checklist/ai_draft/imported) - НОВЕ!
- status (new/confirmed/reported/fixed_pending_retest/retest_passed/retest_failed)
- created_at, updated_at

**Evidence** (докази) - НОВЕ!
- id, issue_id, type (note/code/screenshot/aria_dump/screen_reader_output), content, created_at
- Приклад: type="screen_reader_output", content="NVDA: button"

**Export** (експорт звітів):
- id, project_id, export_type (markdown/docx/json/csv), path, created_at

**Checklist** (чеклісти тестування) - НОВЕ!
- id, name, category, items (JSON array)
- Приклад категорій: Navigation, Forms, Buttons, ARIA, Focus, Semantics
- Items format: `[{"key": "form_label_association", "label": "All inputs have associated labels"}, ...]`

**ChecklistResult** (результати чеклістів) - НОВЕ! СПРОЩЕНО!
- id, session_id, checklist_id, item_key, item_label, status (pass/fail/not_applicable), notes
- Приклад: item_key="form_label_association", item_label="All inputs have labels", status="fail"

---

## 🏗️ ФІНАЛЬНА АРХІТЕКТУРА

```
Project
  └ Target / Flow
       └ TestSession
            └ FindingGroup (НОВЕ!)
                 └ Issue
                      └ Evidence (НОВЕ!)
                      └ Tags (НОВЕ!)
       └ ChecklistResult (НОВЕ!)

Додатково:
- Templates (defect templates)
- Checklists (test checklists)
- Exports
- AI assistant (спрощений)
- Statistics (НОВЕ!)
```

---

## 🚀 ЕТАПИ ВИКОНАННЯ

### PHASE 1: REFRAME + DATA CORE (3-5 днів)
**Мета:** Перебудувати фундамент під нову модель

**Завдання:**
1. ✅ Оновити документацію (ROADMAP, BIG_PICTURE, ARCHITECTURE)
2. ✅ Спроектувати нову модель даних (DATA_MODEL.md)
3. ✅ Міграція з JSON → SQLite
4. ✅ Зберегти сумісність з існуючими даними
5. ✅ Прибрати "$5 за тест" та ігрову економіку
6. ✅ Створити MIGRATION_PLAN.md

**Результат:**
- SQLite база з новими таблицями (включно з FindingGroup, Evidence, Checklist)
- Міграційний скрипт для старих даних
- Оновлена документація

---

### PHASE 2: ISSUE WORKFLOW (10-14 днів) ⚠️ ОНОВЛЕНО
**Мета:** Професійний workflow для роботи з дефектами

**Завдання:**
1. ✅ CRUD для Projects
2. ✅ CRUD для Targets/Flows
3. ✅ Test Sessions
4. ✅ FindingGroups (організація issues в групи)
5. ✅ Issues з повною структурою + tags
6. ✅ Evidence (screen reader output, код, нотатки)
7. ✅ Статуси життєвого циклу
8. ✅ Quick Capture (швидкий ввід нотатки)
9. ✅ Structured Report (повна форма)
10. ✅ Фільтри по tags, severity, status

**Два режими захоплення:**

**Quick Capture:**
```
Вхід: "submit button unlabeled in checkout"
→ Зберігається як raw_note
→ Можна доповнити пізніше
```

**Structured Report:**
```
- Issue title
- Raw note
- Description
- Steps to reproduce
- Observed behavior
- Expected behavior
- User impact
- Severity
- Confidence
- Affected element
- WCAG criterion
- Suggested fix
```

**Результат:**
- Dashboard з проектами та FindingGroups
- Створення та редагування issues з tags
- Evidence capture (особливо screen reader output)
- Фільтри та пошук по tags
- Retest queue

---

### PHASE 2.5: CHECKLIST SYSTEM (3-5 днів) 🆕 НОВА ФАЗА!
**Мета:** Структуроване тестування з чеклістами

**Завдання:**
1. ✅ Створити базові чеклісти:
   - Navigation (skip link, heading structure, landmark roles)
   - Forms (label association, error identification, focus order)
   - Buttons (accessible name, role, keyboard activation)
   - ARIA (roles, states, properties)
   - Focus (visible focus, logical order, no traps)
   - Semantics (proper HTML, heading hierarchy)
2. ✅ UI для роботи з чеклістами
3. ✅ Відмітки: pass / fail / not applicable
4. ✅ Автоматичне створення issues з failed items
5. ✅ Збереження результатів чеклістів

**Результат:**
- Бібліотека чеклістів
- Швидке структуроване тестування
- Автоматична генерація issues

---

### PHASE 3: EXPORTS + PORTFOLIO (7 днів) ⚠️ ОНОВЛЕНО
**Мета:** Генерація професійних звітів

**Завдання:**
1. ✅ Markdown export (developer report)
2. ✅ JSON/CSV export
3. ✅ Client summary report (з statistics!)
4. ✅ Developer issue list (з Evidence)
5. ✅ Portfolio mode (anonymize)
6. ✅ Sample reports для портфоліо
7. ✅ Statistics dashboard (НОВЕ!)
8. ⏳ DOCX export (ОПЦІОНАЛЬНО, пізніше)

**Пріоритет експортів для MVP:**
- ✅ **Обов'язково:** Markdown, JSON, CSV
- ⏳ **Опціонально пізніше:** DOCX

**Statistics для портфоліо:**
- Projects tested
- Issues found (total, by severity)
- Critical issues resolved
- **WCAG criteria referenced in findings** (замість "coverage")
- **WCAG issue distribution** (які критерії найчастіше)
- Average issues per page
- Most common issue types
- Evidence collected

**Формати звітів:**

**Developer Report:**
- Issues в reproducible форматі
- Steps, observed, expected, impact
- WCAG критерії
- Suggested fixes
- **Evidence (screen reader output, код)**
- **Tags для фільтрації**

**Client Summary:**
- Project name
- Tested targets
- Summary of findings **з statistics**
- Issue counts by severity
- **FindingGroups breakdown**
- **WCAG criteria referenced in findings** (не "coverage"!)
- Key blockers
- Recommended next steps

**Результат:**
- Експорт у 3 форматах (Markdown, JSON, CSV)
- DOCX опціонально пізніше
- Готові sample reports
- Portfolio assets
- **Statistics dashboard для демонстрації експертизи**

---

### PHASE 4: AI ASSISTANT (5 днів) ⚠️ СПРОЩЕНО
**Мета:** AI Bug Composer - перетворення нотаток у звіти

**СПРОЩЕНІ пріоритети AI (тільки 3!):**

**Priority 1:** Raw note → Structured defect draft ✅
```
Вхід: "submit button unlabeled in checkout, NVDA says button only"

Вихід:
- Title: Unlabeled Submit Button in Checkout Form
- Steps: Navigate to checkout, tab to submit button
- Observed: NVDA announces "button" without label
- Expected: Should announce button purpose
- Impact: Users cannot identify button function
- WCAG: 4.1.2 Name, Role, Value (Level A)
- Suggested tags: button, screen-reader, forms
- Fix: Add aria-label="Submit order" or visible text
```

**Priority 2:** Suggest template ✅
- Розпізнати тип проблеми
- Запропонувати шаблон з бібліотеки

**Priority 3:** Suggest WCAG criterion ✅
- На основі опису проблеми
- З позначкою uncertainty

**ВСЕ! Більше нічого.**

**НЕ робимо:**
- ❌ Report validation
- ❌ Complex remediation generator
- ❌ Complex reasoning
- ❌ Вигадування фактів

**КРИТИЧНО:**
- AI НЕ вигадує факти
- Режим "structure only"
- Позначати uncertainty clearly: "Probable WCAG: 4.1.2 (confidence: 80%)"
- Розрізняти observed fact vs probable interpretation

**Завдання:**
1. ✅ Defect template library (15-20 типових проблем)
2. ✅ AI endpoint для polishing (тільки 3 функції!)
3. ✅ Safe prompting strategy
4. ✅ Uncertainty labels
5. ✅ Template suggestion
6. ✅ WCAG suggestion з confidence level

**Результат:**
- Швидке перетворення нотаток у звіти
- Бібліотека шаблонів
- AI-асистент з безпечними промптами (БЕЗ overengineering)

---

### PHASE 5: HARDENING (1-2 тижні)
**Мета:** Безпека та надійність

**Завдання:**
1. ✅ Basic auth або аналог
2. ✅ HTTPS (Let's Encrypt)
3. ✅ .env strategy
4. ✅ Config template
5. ✅ Backup strategy для SQLite
6. ✅ CLI для backup/restore
7. ✅ Rate limiting
8. ✅ Debug exposure check
9. ✅ Deployment improvements

**Результат:**
- Безпечна система
- Автоматичні backup
- Production-ready deployment

---

## 📚 DEFECT TEMPLATE LIBRARY

**Типові проблеми (15-20 шаблонів):**

1. Unlabeled button
2. Unlabeled form field
3. Missing heading structure
4. Keyboard inaccessible custom control
5. Ambiguous link text
6. Focus not moved to dialog
7. No focus trap in modal
8. State change not announced
9. Missing error identification
10. Missing skip link
11. Data table header association problems
12. Image without alt / wrong alt
13. Custom widget without semantics
14. Expandable control state not announced
15. Color contrast insufficient
16. Form validation not announced
17. Live region missing
18. Keyboard focus not visible
19. Tab order illogical
20. ARIA role incorrect

**Для кожного шаблону:**
- template_id, category
- default title
- typical description skeleton
- typical impact
- likely WCAG mappings
- possible suggested fix skeleton
- **suggested tags** (НОВЕ!)
- **typical evidence type** (НОВЕ!)

---

## 🧪 CHECKLIST SYSTEM (НОВЕ!)

**Базові чеклісти:**

### Navigation Checklist
- [ ] Skip link present and functional
- [ ] Heading structure logical (h1 → h2 → h3)
- [ ] Landmark roles present (header, nav, main, footer)
- [ ] Focus order follows visual order
- [ ] All interactive elements keyboard accessible

### Forms Checklist
- [ ] All inputs have associated labels
- [ ] Error identification clear
- [ ] Error suggestions provided
- [ ] Focus order logical
- [ ] Required fields indicated
- [ ] Form validation announced

### Buttons Checklist
- [ ] All buttons have accessible name
- [ ] Role="button" or <button> element
- [ ] Keyboard activation (Enter/Space)
- [ ] Focus visible
- [ ] State changes announced

### ARIA Checklist
- [ ] ARIA roles appropriate
- [ ] ARIA states correct
- [ ] ARIA properties present
- [ ] No ARIA where HTML sufficient
- [ ] Live regions for dynamic content

### Focus Management Checklist
- [ ] Focus visible at all times
- [ ] Logical focus order
- [ ] No keyboard traps
- [ ] Focus moved to modals
- [ ] Focus returned after modal close

### Semantics Checklist
- [ ] Proper HTML elements used
- [ ] Heading hierarchy correct
- [ ] Lists marked up as lists
- [ ] Tables have proper headers
- [ ] Regions have labels

**Використання:**
1. Обрати checklist для flow
2. Відмітити pass/fail/N/A
3. Автоматично створити issues з failed items
4. Додати evidence до кожного issue

---

## 🖥️ DASHBOARD ПЕРЕРОБКА

**Нові екрани:**
1. Projects list
2. Project details
3. Targets/pages/flows
4. New test session
5. Quick issue capture
6. Issue list with filters
7. Issue detail editor
8. Export reports
9. Retest queue

**Вимоги:**
- ✅ Keyboard-first
- ✅ NVDA-friendly
- ✅ Logical heading structure
- ✅ Landmarks
- ✅ Accessible modals
- ✅ Hotkeys як enhancement, не єдиний механізм

---

## 💼 COMMERCIALIZATION

**Створити SERVICES.md:**

**Послуги, які можна продавати:**
1. Quick Blind Accessibility Check (1 сторінка/flow)
2. Screen Reader Smoke Test (критичний шлях)
3. Accessibility Bug Report Pack (повний аудит)
4. Retest Service (перевірка фіксів)

**Deliverables:**
- Developer-ready issue reports
- Client summary
- WCAG compliance assessment
- Remediation recommendations

---

## 🎓 CAREER SUPPORT

**Створити CAREER_STRATEGY.md:**

**Як проект допомагає кар'єрі:**
- Доказ технічної експертизи
- Portfolio з реальними звітами
- Proof of workflow
- Демонстрація AI-assisted approach
- Показує production mindset

**Job titles:**
- Accessibility QA Engineer
- Accessibility Tester
- Assistive Technology Specialist
- Blind User Testing Expert
- WCAG Compliance Specialist

**Career assets папка:**
- Sample reports
- Professional positioning
- Value proposition
- CV bullet points
- LinkedIn proof points

---

## 📋 ДОКУМЕНТИ ДЛЯ СТВОРЕННЯ/ОНОВЛЕННЯ

1. ✅ README.md - оновити під нову мету
2. ✅ ROADMAP.md - новий план
3. ✅ BIG_PICTURE.md - нове позиціонування
4. ✅ ARCHITECTURE.md - нова архітектура
5. ✅ DATA_MODEL.md - схема бази
6. ✅ MIGRATION_PLAN.md - план міграції
7. ✅ SERVICES.md - продаваємі послуги
8. ✅ CAREER_STRATEGY.md - кар'єрна стратегія
9. ✅ AI_ASSISTANT_PLAN.md - AI промпти та логіка
10. ✅ DEFECT_TEMPLATES.md - бібліотека шаблонів

---

## 🎨 СТИЛЬ РОБОТИ

### Принципи:
1. **Execution, не brainstorming** - робити, не обговорювати
2. **Маленькі безпечні зміни** - часті коміти
3. **Ітеративний підхід** - працюючий код на кожному етапі
4. **Практичність > краса** - надійність важливіша за красу
5. **Не чекати підтвердження** - якщо рішення очевидне

### Після кожного етапу повідомляти:
- ✅ Progress (що зроблено)
- ✅ Changed files (які файли змінено)
- ✅ How to test (як протестувати)
- ✅ Next task (наступне завдання)

---

## 🚫 ЖОРСТКІ ОБМЕЖЕННЯ

1. ✅ Система залишається usable з NVDA та клавіатурою
2. ✅ Не ламати працюючий dashboard без migration path
3. ✅ Не тягнути важкі залежності без необхідності
4. ✅ Спочатку локальна надійність, потім зовнішні інтеграції
5. ✅ Ніяких "розумних" AI-функцій, які вигадують проблеми
6. ✅ Всі AI suggestions чітко позначені як suggestions
7. ✅ Не будувати багатокористувацьку архітектуру раніше часу
8. ✅ Ніяких складних frontend-фреймворків, якщо можна простіше
9. ✅ Кожен екран має heading structure та keyboard flow
10. ✅ Код та документи пояснюють, як проект допомагає кар'єрі

---

## 🎯 ПРАКТИЧНИЙ РЕЗУЛЬТАТ

**Що я зможу робити після завершення:**
1. ✅ Створити проект для клієнта
2. ✅ Додати URL/flows для тестування
3. ✅ Почати тестову сесію
4. ✅ Швидко фіксувати баги (Quick Capture)
5. ✅ Довести їх до професійного вигляду
6. ✅ Експортувати developer-ready report
7. ✅ Експортувати client summary
8. ✅ Зберегти sample report в портфоліо
9. ✅ Показати систему роботодавцю як proof of workflow
10. ✅ Брати платні замовлення

---

## 📊 МЕТРИКИ УСПІХУ (ОНОВЛЕНО!)

**Замість "$5 за тест":**

### Dashboard Statistics:
- **Projects:** Total tested, active, completed
- **Issues:** Total found, by severity (critical/serious/moderate/minor)
- **WCAG criteria referenced in findings** (не "coverage"!)
- **WCAG issue distribution** (які критерії найчастіше зустрічаються)
- **Average issues per page/flow**
- **Most common issue types** (з tags)
- **Evidence collected:** Screen reader outputs, code snippets
- **Resolution rate:** Fixed vs pending
- **Retest success rate**
- **Issue sources:** Manual vs checklist vs AI-assisted

### Portfolio Metrics (для роботодавців):
- "Tested 15+ projects"
- "Found 200+ accessibility issues"
- "85% critical issues resolved"
- "WCAG 2.2 AA specialist"
- "Specialized in form accessibility and ARIA"
- "Issues referenced 35 different WCAG criteria"

### Export для CV:
```
Accessibility Testing Portfolio
- Projects audited: 15
- Critical issues identified: 45
- WCAG criteria encountered: 1.3.1, 2.4.3, 4.1.2, and 32 others
- Most common findings: Form labels (18%), Focus management (15%), ARIA (12%)
- Tools: NVDA, WCAG 2.2, AI-assisted reporting
- Evidence: 150+ screen reader outputs documented
```

---

## 🔄 ПОРЯДОК ВИКОНАННЯ (ОНОВЛЕНО!)

### Крок 1: Документація (сьогодні)
- Оновити всі документи
- Створити нові (ARCHITECTURE, DATA_MODEL, SERVICES, CAREER_STRATEGY)

### Крок 2: SQLite + Data Model (1-2 дні)
- Створити схему бази (з FindingGroup, Evidence, Checklist)
- Міграційний скрипт
- Repository layer

### Крок 3: Project Workflow (3-4 дні)
- Projects CRUD
- Targets CRUD
- FindingGroups CRUD
- Sessions

### Крок 4: Issue System (4-5 днів)
- Issues базовий CRUD
- Tags system
- Evidence capture
- Фільтри

### Крок 5: Issue Capture (2-3 дні)
- Quick Capture форма
- Structured Report форма
- Статуси

### Крок 6: Checklist System (3-5 днів) 🆕
- Базові чеклісти (6 категорій)
- UI для чеклістів
- Автоматична генерація issues

### Крок 7: Exports (3-4 дні)
- Markdown export
- JSON/CSV export
- Client summary з statistics
- Developer report з evidence
- DOCX опціонально (не для MVP!)

### Крок 8: Statistics Dashboard (2-3 дні) 🆕
- Метрики проектів
- WCAG criteria referenced (не coverage!)
- Issue breakdown
- Issue sources (manual/checklist/AI)
- Portfolio export

### Крок 9: Templates (1-2 дні)
- Defect template library (20 шаблонів)
- Template selection UI

### Крок 10: AI Assistant (3-5 днів)
- AI endpoint (тільки 3 функції!)
- Prompting strategy
- Integration в UI

### Крок 11: Hardening (2-3 дні)
- Auth
- Backup
- Security
- Deployment

**ЗАГАЛЬНИЙ ЧАС: 3-4 тижні** (реалістично!)

---

## 🎬 ПЕРШЕ КОНКРЕТНЕ ДІЙСТВО

**Зараз зроблю:**
1. ✅ Audit поточного проекту
2. ✅ Створити цей план (EXECUTION_PLAN.md)
3. ⏳ Оновити ROADMAP.md
4. ⏳ Оновити BIG_PICTURE.md
5. ⏳ Створити ARCHITECTURE.md
6. ⏳ Створити DATA_MODEL.md
7. ⏳ Створити MIGRATION_PLAN.md
8. ⏳ Створити SERVICES.md
9. ⏳ Створити CAREER_STRATEGY.md

**Потім:**
- SQLite schema
- Migration script
- Початок Phase 1

---

## ✅ ФІНАЛЬНЕ ЗАТВЕРДЖЕННЯ

**ПЛАН ГОТОВИЙ ДО СТАРТУ!**

### Останні правки внесено:

1. ✅ **ChecklistResult спрощено** - item_key + item_label (без окремої таблиці ChecklistItem)
2. ✅ **DOCX відкладено** - MVP: тільки Markdown, JSON, CSV
3. ✅ **"WCAG coverage" замінено** на "WCAG criteria referenced in findings"
4. ✅ **issue.source_type додано** - manual/checklist/ai_draft/imported

### Що НЕ робимо зараз (щоб не зірватись):
- ❌ Multi-user
- ❌ Billing
- ❌ RBAC
- ❌ Jira integration
- ❌ Складна AI-логіка
- ❌ "Ідеальна" аналітика

### Оцінка плану:
**ФІНАЛЬНА:** 9.5/10 ✅

**Готовий починати Phase 1:**
1. Оновити DATA_MODEL.md
2. Оновити ROADMAP.md
3. Оновити BIG_PICTURE.md
4. Оновити ARCHITECTURE.md
5. Почати SQLite + migration

**Чекаю команди START! 🚀**

---

**Статус:** 🟢 Готовий до старту  
**Наступний крок:** Оновлення документації → Phase 1  
**Загальний час:** 3-4 тижні (реалістично)
