# A11y Workbench - Руководство пользователя

## Что это такое?

A11y Workbench - это система для управления процессом тестирования доступности сайтов. Она помогает:
- Быстро записывать проблемы во время тестирования
- Организовывать работу по проектам
- Создавать профессиональные отчеты для клиентов
- Вести статистику своей работы

---

## Как работать с системой

### Шаг 1: Создай проект

Когда получаешь новый заказ на тестирование:

1. Открой http://34.58.51.76:8000/dashboard
2. Нажми "➕ New Project"
3. Заполни:
   - **Project Name:** "Банк ABC - Accessibility Audit"
   - **Client Name:** "Банк ABC"
   - **Description:** "Полный аудит доступности сайта"
   - **Status:** Active

**Результат:** Проект появится в списке, можно начинать работу.

---

### Шаг 2: Добавь цели тестирования

Определи что именно будешь тестировать:

1. Открой проект
2. Нажми "➕ Add Target"
3. Примеры целей:
   - **Name:** "Login page", **Type:** Page, **URL:** https://bank.com/login
   - **Name:** "Registration form", **Type:** Form, **URL:** https://bank.com/register
   - **Name:** "Main navigation", **Type:** Component
   - **Name:** "Checkout flow", **Type:** Flow

**Результат:** Список всех страниц/компонентов для тестирования.

---

### Шаг 3: Начни тест-сессию

Перед началом тестирования запиши параметры:

1. Выбери цель (например "Login page")
2. Нажми "🧪 Start Session"
3. Заполни:
   - **Session Name:** "Login page - NVDA testing"
   - **Tools Used:** "NVDA 2024.1, Chrome 120, Windows 11"
   - **Notes:** "Testing keyboard navigation and form labels"

**Результат:** Система запомнит когда и с какими инструментами ты тестировал.

---

### Шаг 4: Записывай проблемы

Во время тестирования нашел проблему? Есть 2 способа:

#### Способ A: Быстрая запись (во время теста)

Используй когда нужно быстро зафиксировать проблему:

1. Нажми "⚡ Quick Capture"
2. Заполни минимум:
   - **Title:** "Submit button unlabeled"
   - **Quick Notes:** "NVDA announces 'button' without label"
   - **Severity:** Serious
3. Нажми "Save"

**Время:** 10-15 секунд

#### Способ B: Детальная запись (после теста)

Используй для полного описания проблемы:

1. Нажми "➕ Add Issue"
2. Заполни все поля:
   - **Title:** "Submit button missing accessible name"
   - **Description:** "The submit button in login form has no accessible name"
   - **Severity:** Serious
   - **Status:** New
   - **WCAG Criterion:** 4.1.2 Name, Role, Value
   - **Steps to Reproduce:**
     ```
     1. Navigate to login page
     2. Tab to submit button
     3. Listen to NVDA announcement
     ```
   - **Expected Behavior:** "NVDA should announce 'Submit button' or 'Login button'"
   - **Actual Behavior:** "NVDA announces only 'button' without label"

**Время:** 2-3 минуты

---

### Шаг 5: Добавь доказательства

Для каждой проблемы можно добавить доказательства:

1. Открой issue (нажми на заголовок)
2. Нажми "➕ Add Evidence"
3. Выбери тип:

**🔊 Screen Reader Output:**
```
NVDA: "Button"
Expected: "Submit button" or "Login button"
```

**💻 Code Snippet:**
```html
<!-- Problem: -->
<button type="submit"></button>

<!-- Solution: -->
<button type="submit">Login</button>
<!-- or -->
<button type="submit" aria-label="Login">
  <span class="icon-arrow"></span>
</button>
```

**🏷️ ARIA Info:**
```
Role: button
Name: (empty)
State: (none)
```

**📝 Notes:**
```
This affects all screen reader users.
Similar issue found on registration page.
```

**Результат:** Разработчик получит все данные для исправления.

---

### Шаг 6: Экспортируй отчет

Когда тестирование завершено:

1. Нажми "📥 Export" на проекте
2. Выбери формат:

#### 📄 Markdown (для разработчиков)
```markdown
# Accessibility Report: Банк ABC

## Summary
- Total Issues: 15
- Critical: 2
- Serious: 5
- Moderate: 6
- Minor: 2

## Critical Issues (2)

### 1. Login form not keyboard accessible
**WCAG:** 2.1.1 Keyboard
**Status:** New

**Description:** Cannot access login form using keyboard only

**Steps to Reproduce:**
1. Navigate to login page
2. Try to tab to username field
3. Focus skips the form

**Evidence:**
Code snippet:
<div onclick="showLogin()">Login</div>
```

#### 📊 JSON (для интеграции)
```json
{
  "project": {
    "name": "Банк ABC",
    "total_issues": 15
  },
  "issues": [
    {
      "title": "Login form not keyboard accessible",
      "severity": "critical",
      "wcag": "2.1.1",
      "evidence": [...]
    }
  ]
}
```

#### 📋 CSV (для Excel)
```
ID,Title,Severity,Status,WCAG,Created
1,Login form not keyboard accessible,critical,new,2.1.1,2026-03-07
2,Submit button unlabeled,serious,new,4.1.2,2026-03-07
```

#### 📈 Statistics (для клиента)
```
Project: Банк ABC
Total Issues: 15

By Severity:
- Critical: 2
- Serious: 5
- Moderate: 6
- Minor: 2

By Status:
- New: 10
- Confirmed: 3
- Fixed: 2

WCAG Criteria: 2.1.1, 2.4.3, 4.1.2, 1.3.1, 2.4.7
```

---

## Полный пример работы

### Сценарий: Аудит сайта интернет-магазина

**День 1: Подготовка**
```
1. Создаю проект "E-Shop - Accessibility Audit"
2. Добавляю цели:
   - Homepage
   - Product catalog
   - Product page
   - Shopping cart
   - Checkout flow
```

**День 2-3: Тестирование**
```
Утро:
- Начинаю сессию "Homepage - NVDA + Chrome"
- Быстро записываю 5 проблем через Quick Capture
- Добавляю детали после обеда

Вечер:
- Начинаю сессию "Product catalog - JAWS + Firefox"
- Нахожу 3 проблемы
- Сразу добавляю code snippets и screen reader output
```

**День 4: Отчет**
```
1. Открываю проект
2. Проверяю все issues (всего 23)
3. Добавляю недостающие доказательства
4. Экспортирую Markdown отчет
5. Отправляю клиенту
```

**Результат:**
- Профессиональный отчет на 23 проблемы
- Время работы: 3 дня
- Клиент доволен
- Отчет добавляю в портфолио

---

## Дополнительные возможности

### Фильтры и поиск

**Фильтры:**
- По severity: показать только Critical и Serious
- По status: показать только New issues
- По WCAG: показать все проблемы 2.4.x

**Поиск:**
- Введи "button" - найдет все issues про кнопки
- Введи "keyboard" - найдет все проблемы с клавиатурой

### Глобальная статистика

В header dashboard видишь:
- **Projects:** 5 (всего проектов)
- **Total Issues:** 87 (всего проблем найдено)
- **Critical:** 12 (критических проблем)
- **Serious:** 28 (серьезных проблем)
- **WCAG Criteria:** 23 (разных критериев WCAG)

**Используй для:**
- CV: "Провел 5 аудитов, нашел 87 проблем доступности"
- Портфолио: "Опыт работы с 23 критериями WCAG 2.2"

---

## Советы по работе

### Во время тестирования:
1. **Используй Quick Capture** - не отвлекайся на детали
2. **Записывай сразу** - не надейся на память
3. **Группируй похожие проблемы** - "All buttons unlabeled" вместо 10 отдельных issues

### После тестирования:
1. **Добавь детали** - WCAG, шаги, ожидаемое поведение
2. **Приложи доказательства** - код, screen reader output
3. **Проверь статус** - все ли issues записаны

### Перед отправкой отчета:
1. **Проверь severity** - правильно ли оценил критичность
2. **Проверь WCAG** - правильно ли указал критерии
3. **Проверь описания** - понятно ли разработчику

---

## Частые вопросы

**Q: Можно ли редактировать issues?**
A: Да, нажми на issue и отредактируй любое поле.

**Q: Можно ли удалить issue?**
A: Да, нажми "Delete" в детальном виде issue.

**Q: Можно ли работать с несколькими проектами одновременно?**
A: Да, создавай сколько угодно проектов.

**Q: Можно ли экспортировать все проекты сразу?**
A: Нет, экспорт работает по одному проекту. Но можно экспортировать глобальную статистику.

**Q: Нужен ли интернет для работы?**
A: Да, система работает через браузер на сервере.

**Q: Можно ли работать с телефона?**
A: Технически да, но удобнее с компьютера.

---

## Контакты и поддержка

**Система:** http://34.58.51.76:8000/dashboard  
**GitHub:** https://github.com/abuten1977-design/a11y-workbench  
**Автор:** Andriy Butenko (abuten1977@gmail.com)

---

*Последнее обновление: 2026-03-07*
