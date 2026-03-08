# Пошаговая инструкция: Аудит lifeindenmark.borger.dk

## 🎯 Проект: Life in Denmark Portal Accessibility Audit

**Сайт:** https://lifeindenmark.borger.dk/  
**Дата:** 8 марта 2026  
**Тестировщик:** Andriy Butenko  
**Инструменты:** NVDA 2024.1, Chrome, axe-core 4.11.1

---

## 📊 Результаты axe-core (автоматическая проверка)

**Главная страница:**
- ✅ Violations: 0
- ✅ Passes: 31 checks
- ⚠️ Incomplete: 1 (требует ручной проверки)

**Вывод:** Сайт технически хорошо сделан, но автоматика проверяет только ~30% проблем.  
**Задача:** Найти проблемы которые axe не видит (keyboard navigation, screen reader UX, focus management)

---

## 📝 ШАГ 1: Создай проект в системе

### Действия:

1. **Открой dashboard:**
   ```
   http://34.58.51.76:8000/dashboard
   ```

2. **Нажми кнопку:** "➕ New Project"

3. **Заполни форму:**
   ```
   Project Name: Life in Denmark - Accessibility Audit
   Client Name: Borger.dk (Demo)
   Description: Accessibility audit of the Life in Denmark portal for international citizens. Focus on WCAG 2.2 Level AA compliance and screen reader usability.
   Status: Active
   ```

4. **Нажми:** "Create Project"

5. **Результат:** Проект появится в списке

---

## 📝 ШАГ 2: Добавь цели тестирования (Targets)

### Что тестировать:

1. **Target 1: Homepage**
   ```
   Name: Homepage
   Type: Page
   URL: https://lifeindenmark.borger.dk/
   Description: Main landing page with navigation and search
   ```

2. **Target 2: Housing and Moving**
   ```
   Name: Housing and Moving
   Type: Page
   URL: https://lifeindenmark.borger.dk/housing-and-moving
   Description: Information page about housing
   ```

3. **Target 3: Working in Denmark**
   ```
   Name: Working in Denmark
   Type: Page
   URL: https://lifeindenmark.borger.dk/working
   Description: Information about work permits and employment
   ```

4. **Target 4: Main Navigation**
   ```
   Name: Main Navigation Menu
   Type: Component
   URL: https://lifeindenmark.borger.dk/
   Description: Top navigation with dropdown menus
   ```

5. **Target 5: Search Function**
   ```
   Name: Search Functionality
   Type: Component
   URL: https://lifeindenmark.borger.dk/
   Description: Site search feature
   ```

### Как добавить:
- Открой проект
- Нажми "➕ Add Target"
- Заполни данные
- Повтори для всех 5 целей

---

## 📝 ШАГ 3: Начни тест-сессию

### Для каждой цели создай сессию:

**Пример для Homepage:**

1. **Нажми на Target:** "Homepage"
2. **Нажми:** "🧪 Start Session"
3. **Заполни:**
   ```
   Session Name: Homepage - NVDA + Chrome
   Tools Used: NVDA 2024.1, Chrome 120, Windows 11, axe-core 4.11.1
   Notes: Testing keyboard navigation, screen reader announcements, and focus management. Axe-core found 0 violations - focusing on manual testing.
   ```
4. **Нажми:** "Start Session"

---

## 📝 ШАГ 4: Ручное тестирование с NVDA

### Что проверять на каждой странице:

#### A. Keyboard Navigation (клавиатура)
- [ ] Tab order логичный?
- [ ] Все интерактивные элементы доступны?
- [ ] Skip links работают?
- [ ] Dropdown меню открываются с клавиатуры?
- [ ] Нет keyboard traps?

#### B. Screen Reader (NVDA)
- [ ] Заголовки правильные (H1, H2, H3)?
- [ ] Landmarks объявляются (navigation, main, footer)?
- [ ] Ссылки понятные вне контекста?
- [ ] Изображения имеют alt (или decorative)?
- [ ] Формы: labels связаны с полями?
- [ ] Кнопки имеют понятные названия?

#### C. Focus Management
- [ ] Focus visible?
- [ ] Focus не теряется?
- [ ] Focus не прыгает неожиданно?
- [ ] После закрытия модалки focus возвращается?

#### D. Dynamic Content
- [ ] Live regions для обновлений?
- [ ] Ошибки объявляются?
- [ ] Loading states объявляются?

---

## 📝 ШАГ 5: Записывай проблемы

### Когда найдешь проблему:

**Вариант 1: Quick Capture (быстро во время теста)**

1. Нажми "⚡ Quick Capture"
2. Заполни минимум:
   ```
   Title: [Короткое описание]
   Quick Notes: [Что не так]
   Severity: [critical/serious/moderate/minor]
   ```
3. Save

**Вариант 2: Detailed Issue (после теста)**

1. Нажми "➕ Add Issue"
2. Заполни все поля (я помогу!)

---

## 📝 ШАГ 6: Примеры проблем для поиска

### Типичные проблемы которые axe НЕ находит:

#### 🔴 CRITICAL:
- Keyboard trap в меню
- Форма не работает с клавиатуры
- Контент недоступен для screen reader

#### 🟠 SERIOUS:
- Skip link не работает
- Focus не виден
- Dropdown меню не объявляется
- Ошибки формы не читаются

#### 🟡 MODERATE:
- Tab order нелогичный
- Ссылки "Read more" без контекста
- Заголовки пропущены
- Alt текст есть но бессмысленный

#### 🟢 MINOR:
- Redundant ARIA
- Лишние объявления
- Мелкие UX проблемы

---

## 📝 ШАГ 7: Как я буду помогать

### Ты говоришь мне:

```
"Нашел проблему: dropdown меню не открывается с клавиатуры"
```

### Я даю тебе:

```
Title: Main navigation dropdown not keyboard accessible
Severity: serious
WCAG: 2.1.1 Keyboard

Description: The dropdown menus in the main navigation cannot be opened using keyboard only. Users must use a mouse to access submenu items.

Steps to Reproduce:
1. Navigate to https://lifeindenmark.borger.dk/
2. Press Tab to reach main navigation
3. Try to open dropdown menu using Enter, Space, or Arrow keys
4. Menu does not open

Expected Behavior: 
Dropdown menus should open when focused and Enter/Space is pressed, or Arrow Down key should open and navigate submenu items.

Actual Behavior:
Dropdown menus only open on mouse hover. Keyboard users cannot access submenu items.

User Impact:
Keyboard-only users and screen reader users cannot access important navigation links, making large portions of the site unreachable.

Suggested Fix:
Add keyboard event handlers (onKeyDown) to menu items. Implement ARIA menu pattern or use native HTML disclosure widgets.
```

### Ты копируешь в систему ✅

---

## 📝 ШАГ 8: Добавь Evidence (доказательства)

### Для каждой проблемы добавь:

1. **Открой issue** (нажми на заголовок)
2. **Нажми:** "➕ Add Evidence"
3. **Выбери тип:**

**🔊 Screen Reader Output:**
```
NVDA: "Link, Housing and Moving"
[Press Enter]
NVDA: "Link, Housing and Moving"
Expected: Menu should open and announce submenu items
```

**💻 Code Snippet:**
```html
<!-- Current code: -->
<a href="/housing-and-moving" class="menu-item">
  Housing and Moving
</a>

<!-- Missing: keyboard handler and ARIA -->
```

**📝 Notes:**
```
Tested with NVDA 2024.1 and Chrome 120.
Same issue on all main navigation items.
Mouse hover works correctly.
```

---

## 📝 ШАГ 9: Тестируй все цели

Повтори Шаги 3-8 для каждой цели:
- ✅ Homepage
- ✅ Housing and Moving
- ✅ Working in Denmark
- ✅ Main Navigation
- ✅ Search Function

---

## 📝 ШАГ 10: Экспортируй отчет

### Когда все протестировано:

1. **Открой проект**
2. **Нажми:** "📥 Export"
3. **Выбери формат:**

**Markdown** - для разработчиков:
```markdown
# Accessibility Report: Life in Denmark Portal

## Summary
- Total Issues: 12
- Critical: 2
- Serious: 4
- Moderate: 5
- Minor: 1

## Critical Issues
1. Search form not keyboard accessible
2. Cookie banner keyboard trap
...
```

**JSON** - для интеграции:
```json
{
  "project": "Life in Denmark - Accessibility Audit",
  "issues": [...]
}
```

**CSV** - для Excel:
```
ID,Title,Severity,Status,WCAG,Created
1,Search form not keyboard accessible,critical,new,2.1.1,2026-03-08
```

4. **Сохрани файл**
5. **Добавь в портфолио**

---

## 📝 ШАГ 11: Статистика для CV

### Посмотри статистику:

1. **Нажми:** "📈 Stats" на проекте
2. **Увидишь:**
   ```
   Project: Life in Denmark - Accessibility Audit
   Total Issues: 12
   
   By Severity:
   - Critical: 2
   - Serious: 4
   - Moderate: 5
   - Minor: 1
   
   WCAG Criteria: 2.1.1, 2.4.1, 2.4.3, 4.1.2, 1.3.1
   ```

3. **Используй в CV:**
   ```
   "Conducted accessibility audit of Danish government portal
   - Found 12 WCAG 2.2 violations (2 critical, 4 serious)
   - Tested with NVDA and automated tools (axe-core)
   - Covered 5 WCAG criteria
   - Delivered professional report with code examples"
   ```

---

## 🎯 Чек-лист готовности отчета

Перед экспортом проверь:

- [ ] Все цели протестированы
- [ ] Каждая проблема имеет severity
- [ ] Каждая проблема имеет WCAG критерий
- [ ] Добавлены steps to reproduce
- [ ] Добавлены evidence (screen reader output, код)
- [ ] Проверена орфография
- [ ] Статус issues актуален

---

## 💡 Советы

### Во время тестирования:
1. **Используй Quick Capture** - не останавливайся на деталях
2. **Записывай сразу** - не полагайся на память
3. **Делай скриншоты** - пригодятся для evidence
4. **Тестируй систематически** - по чек-листу из Шага 4

### После тестирования:
1. **Добавь детали** - я помогу с формулировками
2. **Добавь evidence** - код, screen reader output
3. **Проверь WCAG** - правильно ли указал критерии
4. **Проверь severity** - соответствует ли user impact

### Для портфолио:
1. **Анонимизируй** - убери личные данные если есть
2. **Добавь методологию** - как тестировал
3. **Покажи разницу** - axe vs ручное тестирование
4. **Добавь статистику** - цифры впечатляют

---

## 🚀 Готов начинать!

**Следующий шаг:**
1. Открой http://34.58.51.76:8000/dashboard
2. Создай проект (Шаг 1)
3. Добавь цели (Шаг 2)
4. Открой https://lifeindenmark.borger.dk/ с NVDA
5. Начинай тестировать!

**Я буду помогать на каждом шаге!** 💪

---

*Документ создан: 8 марта 2026*
