# 🗺️ BIG PICTURE: A11y Workbench

**Версія:** 2.0  
**Дата:** 6 березня 2026

---

## 🎯 ГОЛОВНА МЕТА

**Створити персональну виробничу систему незрячого accessibility-експерта, яка допоможе:**
1. Швидко робити професійні звіти
2. Збирати портфоліо
3. Брати платні замовлення
4. Отримати роботу в Данії / international remote
5. Потім (можливо) перетворити в мікросервіс

**НЕ marketplace, НЕ SaaS, НЕ платформа для багатьох**

---

## 👤 ХТО Я

**Незрячий accessibility-експерт:**
- Реальний досвід незрячого користувача screen reader
- Тренінг Deque
- Технічна база: Linux, Python, AI tools, Git
- Розумію Apple ecosystem (iPhone, Mac)
- Живу в Данії
- Хочу побудувати кар'єру в accessibility testing

**Моя цінність:**
- Не автоматизація, а реальний blind user
- Професійні звіти з WCAG
- NVDA експертиза
- AI-assisted workflow

---

## 📍 ДЕ МИ ЗАРАЗ

### ✅ PHASE 0: Prototype (ЗАВЕРШЕНО)

**Що маємо:**
- FastAPI backend (v0.3.0)
- Dashboard з hotkeys (Alt+1/2/3/0)
- Черга завдань (JSON файли)
- Детальна форма звіту
- WCAG 2.2 база (87 критеріїв)
- Google Cloud сервер (e2-micro, Free Tier)
- Systemd service (24/7)
- Git репозиторій (гілка: server-dashboard)

**Що працює:**
- http://34.58.51.76:8000/dashboard
- Створення завдань через API
- Тестування з NVDA
- Збереження результатів
- 13+ завершених тестів

**Проблема:**
- Модель "job queue", не "project workflow"
- Ігрова економіка "$5 за тест"
- JSON файли замість бази даних
- Немає організації по проектах
- Немає evidence capture
- Немає експорту звітів
- Немає портфоліо режиму

**Висновок:** Робочий прототип, але не готовий для реальних клієнтів

---

### 🔄 PHASE 1: REFRAME + DATA CORE (В ПРОЦЕСІ)

**Термін:** 3-5 днів  
**Статус:** 🔄 Документація

**Що робимо:**
1. Переосмислюємо проект
2. Оновлюємо документацію
3. Проектуємо нову архітектуру
4. Міграція JSON → SQLite
5. Нова модель даних

**Нова модель:**
```
Project (клієнт)
  └ Target (сторінка/flow)
       └ TestSession (сесія тестування)
            └ FindingGroup (група проблем)
                 └ Issue (дефект)
                      └ Evidence (докази)
```

**Результат:**
- Чітка мета
- Нова архітектура
- SQLite база
- Готовність до Phase 2

---

## 🚀 КУДИ ЙДЕМО

### Короткострокова мета (1 місяць)

**Технічна:**
- Завершити A11y Workbench v1.0
- Project-based workflow
- Exports (Markdown/JSON/CSV)
- Statistics dashboard
- AI assistant (базовий)

**Бізнесова:**
- 3-5 sample reports в портфоліо
- Готовність брати замовлення
- CV з доказами експертизи

---

### Середньострокова мета (2-3 місяці)

**Кар'єра:**
- Реєстрація на UserTesting
- Пошук вакансій (Accessibility QA Engineer)
- LinkedIn профіль з портфоліо
- Перші платні замовлення

**Продукт:**
- 10+ завершених проектів
- Статистика для CV
- Відточений workflow
- Можливо перші клієнти

---

### Довгострокова мета (6-12 місяців)

**Кар'єра:**
- Робота в Данії або international remote
- Стабільний дохід
- Репутація експерта

**Продукт (опціонально):**
- Мікросервіс "Blind Accessibility Review"
- API для клієнтів
- Можливо масштабування

---

## 💼 БІЗНЕС-МОДЕЛЬ

### Зараз: Послуги

**Що продаю:**
- Manual screen reader accessibility testing
- Developer-ready issue reports
- WCAG compliance assessment
- Retest after fixes

**Пакети:**
1. **Quick Blind Check** - 1 сторінка ($50-100)
2. **Screen Reader Smoke Test** - критичний flow ($100-200)
3. **Bug Report Pack** - повний аудит ($300-500)
4. **Retest Service** - перевірка фіксів ($50-100)

**Deliverables:**
- Structured issue reports
- WCAG criteria mapping
- Evidence (screen reader output)
- Remediation recommendations

---

### Потім: Мікросервіс (можливо)

**Якщо буде попит:**
- API для автоматичного прийому завдань
- Webhook для результатів
- Підписка для регулярних клієнтів

**Але це НЕ пріоритет зараз!**

---

## 🎯 КОНКУРЕНТНІ ПЕРЕВАГИ

**Чому клієнти оберуть мене:**

1. **Реальний незрячий експерт** - не автоматизація
2. **Deque тренінг** - професійна підготовка
3. **NVDA експертиза** - найпопулярніший безкоштовний screen reader
4. **Детальні звіти** - з WCAG, evidence, remediation
5. **AI-assisted** - швидко, але human-verified
6. **Власна система** - proof of workflow
7. **Ціна** - конкурентна ($50-500 vs $100-150/год на Fable)

---

## 📊 ЯК ВИГЛЯДАЄ УСПІХ

### Через 1 місяць:
- ✅ A11y Workbench v1.0 готовий
- ✅ 3-5 sample reports
- ✅ Statistics для CV
- ✅ Готовий брати замовлення

### Через 3 місяці:
- ✅ 10+ завершених проектів
- ✅ Перші платні клієнти
- ✅ LinkedIn профіль з портфоліо
- ✅ Подано заявки на вакансії

### Через 6 місяців:
- ✅ Робота або регулярні клієнти
- ✅ Стабільний дохід
- ✅ Репутація експерта
- ✅ Можливо масштабування

---

## 🛠️ ТЕХНІЧНА СТРАТЕГІЯ

### Принципи:

1. **Практичність > краса** - надійність важливіша
2. **Execution > brainstorming** - робити, не обговорювати
3. **MVP first** - мінімум для старту
4. **No overengineering** - не будувати зайвого
5. **NVDA-friendly** - доступність обов'язкова

### Що НЕ робимо:
- ❌ Multi-user
- ❌ Billing system
- ❌ RBAC
- ❌ Jira integration
- ❌ Складна AI
- ❌ "Ідеальна" аналітика

### Фокус:
- ✅ Personal production tool
- ✅ Client-ready reporting
- ✅ Portfolio generation
- ✅ Career support

---

## 🎓 КАР'ЄРНА СТРАТЕГІЯ

### Job titles:
- Accessibility QA Engineer
- Accessibility Tester
- Assistive Technology Specialist
- Blind User Testing Expert
- WCAG Compliance Specialist

### Proof points:
- "Built production accessibility testing system"
- "Tested 15+ projects, found 200+ issues"
- "WCAG 2.2 AA specialist"
- "AI-assisted workflow, human-verified"
- "Deque trained, NVDA expert"

### Де шукати:
- UserTesting (international)
- LinkedIn Jobs (Denmark + remote)
- Upwork/Fiverr (фріланс)
- Прямі звернення до компаній

---

## 📋 КЛЮЧОВІ ДОКУМЕНТИ

**Технічні:**
- `ROADMAP.md` - план розробки
- `ARCHITECTURE.md` - технічна архітектура
- `DATA_MODEL.md` - схема бази
- `EXECUTION_PLAN.md` - детальний план

**Бізнесові:**
- `SERVICES.md` - продаваємі послуги
- `CAREER_STRATEGY.md` - кар'єрна стратегія
- `PROJECT_STATUS.md` - поточний статус

**Історичні:**
- `REGISTRATION_PLAN.md` - план реєстрації (застарів)
- `why_server_needed.md` - чому потрібен сервер
- `analiz_rynka_realnost.md` - аналіз ринку

---

## 🎬 НАСТУПНІ КРОКИ

**Сьогодні (Phase 1):**
1. ✅ Оновити ROADMAP
2. ✅ Оновити BIG_PICTURE
3. ⏳ Створити ARCHITECTURE
4. ⏳ Створити DATA_MODEL
5. ⏳ Створити SERVICES
6. ⏳ Створити CAREER_STRATEGY

**Цього тижня:**
- SQLite + нова модель
- Міграція даних
- Початок Phase 2

**Цього місяця:**
- Завершити v1.0
- Sample reports
- Готовність до замовлень

---

## 💡 ГОЛОВНА ДУМКА

**Це не "ще один pet project"**

**Це інструмент, який:**
- Допоможе заробляти
- Доведе експертизу
- Відкриє кар'єру
- Можливо стане бізнесом

**Фокус:** Зробити себе суперефективним експертом з власною системою

**Результат:** Гроші, досвід, кейси, робота

---

**Останнє оновлення:** 6 березня 2026, 18:15 CET  
**Версія:** 2.0 (A11y Workbench)  
**Статус:** Phase 1 - Reframe
