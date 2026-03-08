# Evidence для багов lifeindenmark.borger.dk

## БАГ #1: Skip to main content link targets incorrect location with unlabeled images

**Severity:** Serious  
**WCAG:** 2.4.1 Bypass Blocks

### Evidence Type: Screen Reader Output

```
NVDA output when using skip link:

1. Focus on "Skip to main content" link at top of page
2. Press Enter to activate
3. NVDA announces: "Нет описания, graphic" (3 times in a row)
4. Focus lands on unlabeled images instead of main content

Expected behavior:
Focus should move directly to the beginning of main content area,
skipping all navigation, header elements, and decorative images.

Actual behavior:
Focus moves to a location with 3 unlabeled decorative images,
forcing screen reader users to navigate through them before
reaching actual content.

Testing environment:
- NVDA 2025.3
- Chrome (latest)
- Windows 11
- Date: 2026-03-08
- URL: https://lifeindenmark.borger.dk/
```

### Evidence Type: Code Snippet

```html
<!-- Current implementation (WRONG): -->
<a href="#main">Skip to main content</a>

<!-- The #main anchor is placed BEFORE the unlabeled images -->
<div id="main">
  <img src="..." alt="">  <!-- Unlabeled image 1 -->
  <img src="..." alt="">  <!-- Unlabeled image 2 -->
  <img src="..." alt="">  <!-- Unlabeled image 3 -->
  <!-- Actual content starts here -->
</div>

<!-- Correct implementation: -->
<a href="#main">Skip to main content</a>

<div aria-hidden="true">
  <img src="..." alt="">  <!-- Decorative images hidden from screen readers -->
  <img src="..." alt="">
  <img src="..." alt="">
</div>

<main id="main">
  <!-- Main content starts here -->
  <h1>The official guide to life in Denmark</h1>
  ...
</main>
```

### Evidence Type: Notes

```
This is a SERIOUS issue because:

1. Defeats the purpose of skip link - users still have to navigate through obstacles
2. Unlabeled images create confusion ("What am I looking at?")
3. Violates WCAG 2.4.1 Bypass Blocks - the bypass mechanism doesn't work properly
4. Affects ALL screen reader users on EVERY page visit

Impact on users:
- Keyboard users waste time
- Screen reader users get confused by unlabeled graphics
- Users may think the skip link is broken
- Poor first impression of site accessibility

Recommendation:
Move #main anchor to AFTER decorative images, or mark images as aria-hidden="true"
```

---

## БАГ #2: Topic category icons missing alternative text - links unusable for screen readers

**Severity:** Serious  
**WCAG:** 1.1.1 Non-text Content, 2.4.4 Link Purpose

### Evidence Type: Screen Reader Output

```
NVDA output when navigating topic category links:

"Settle in Denmark, link, Нет описания, graphic"
"Housing and moving, link, Нет описания, graphic"
"Working, link, Нет описания, graphic"
"Family and children, link, Нет описания, graphic"
"Money and tax, link, Нет описания, graphic"
"School and education, link, Нет описания, graphic"
"Healthcare, link, Нет описания, graphic"
"Travel and transport, link, Нет описания, graphic"
"Pension, link, Нет описания, graphic"
"Rights, link, Нет описания, graphic"
"Leisure and networking, link, Нет описания, graphic"
"Digital services, link, Нет описания, graphic"

Pattern: Each topic link contains:
1. Text label (good)
2. Decorative icon with alt="" (causes "Нет описания" announcement)

Expected:
Icons should be marked aria-hidden="true" to prevent announcement,
OR have descriptive alt text that matches the link purpose.

Actual:
Icons have empty alt="" but are NOT marked aria-hidden,
causing NVDA to announce "Нет описания" (No description) for each icon.

Testing environment:
- NVDA 2025.3 (Russian language)
- Chrome (latest)
- Windows 11
- Date: 2026-03-08
- URL: https://lifeindenmark.borger.dk/ (All topics section)
```

### Evidence Type: Code Snippet

```html
<!-- Current implementation (WRONG): -->
<a href="/settle-in-denmark">
  <img src="/-/media/spritemaps/EmnerSpritemap.svg#Udlaendige_i_danmark" alt="">
  Settle in Denmark
</a>

<!-- Problem: alt="" without aria-hidden="true" -->
<!-- Screen readers announce the empty alt as "No description" -->

<!-- Correct implementation - Option 1 (Recommended): -->
<a href="/settle-in-denmark">
  <img src="/-/media/spritemaps/EmnerSpritemap.svg#Udlaendige_i_danmark" 
       alt="" 
       aria-hidden="true">
  Settle in Denmark
</a>

<!-- Correct implementation - Option 2: -->
<a href="/settle-in-denmark">
  <img src="/-/media/spritemaps/EmnerSpritemap.svg#Udlaendige_i_danmark" 
       alt="Settle in Denmark icon">
  Settle in Denmark
</a>
<!-- Note: This creates redundancy but is technically correct -->
```

### Evidence Type: Notes

```
This is a SERIOUS issue because:

1. Affects 12 major navigation links (all topic categories)
2. Creates confusing user experience - "No description" after every link
3. Violates WCAG 1.1.1 - decorative images not properly marked
4. Makes site sound unprofessional and poorly implemented

Impact on users:
- Confusion: "What is 'No description'? Is something broken?"
- Annoyance: Extra announcement after every link
- Inefficiency: Takes longer to navigate
- Trust issues: Site seems poorly made

Why this happens:
Developers used alt="" thinking it would hide the image,
but forgot to add aria-hidden="true". Screen readers
still detect the image and announce it as "No description".

Recommendation:
Add aria-hidden="true" to all decorative icons in links.
This is a simple fix that will improve UX significantly.
```

---

## БАГ #3: Duplicate logo images in header - announced 4 times by screen reader

**Severity:** Moderate  
**WCAG:** 2.4.4 Link Purpose (In Context)

### Evidence Type: Screen Reader Output

```
NVDA output when navigating header from top of page:

"Skip to main content, link"
[Tab]
"Life in Denmark logo, link"
[Tab]
"Life in Denmark logo, link"
[Tab]
"Life in Denmark logo, link"
[Tab]
"Life in Denmark logo, link"
[Tab]
"lifeindenmark.dk, link"
[Tab]
"Digital Post, link"
[Tab]
"Menu, button"

Expected:
Only ONE "Life in Denmark logo" announcement.
Additional logos (if needed for responsive design) should be
hidden from screen readers with aria-hidden="true".

Actual:
FOUR identical "Life in Denmark logo" announcements in a row.
All 4 logos link to the same homepage URL (/).

Testing environment:
- NVDA 2025.3
- Chrome (latest)
- Windows 11
- Date: 2026-03-08
- URL: https://lifeindenmark.borger.dk/
```

### Evidence Type: Code Snippet

```html
<!-- Current implementation (WRONG): -->
<a href="/">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>
<a href="/">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>
<a href="/">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>
<a href="/">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>

<!-- All 4 logos are identical and all link to homepage -->

<!-- Correct implementation - Option 1 (Best): -->
<a href="/">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>
<!-- Keep only one logo, remove duplicates -->

<!-- Correct implementation - Option 2 (If responsive design requires multiple): -->
<a href="/" class="logo-desktop">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="Life in Denmark logo">
</a>
<a href="/" class="logo-mobile" aria-hidden="true">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="">
</a>
<a href="/" class="logo-tablet" aria-hidden="true">
  <img src="/-/media/Borger/Logo/2018/LID_dk.svg" alt="">
</a>
<!-- Hide responsive variants from screen readers -->
```

### Evidence Type: Notes

```
This is a MODERATE issue because:

1. Creates annoying but not blocking user experience
2. Wastes user time - 4 tab stops instead of 1
3. Makes site seem poorly implemented
4. Confusing - users may think they're stuck in a loop

Impact on users:
- Keyboard users: 3 extra tab stops to skip
- Screen reader users: Hear same announcement 4 times
- Confusion: "Why is this repeating? Am I stuck?"
- Frustration: "This site is annoying to navigate"

Why this happens:
Likely a responsive design issue where logos are shown/hidden
with CSS for different screen sizes, but all remain in the DOM
and accessible to screen readers.

Recommendation:
1. Audit header HTML - why are there 4 logos?
2. If for responsive design: keep only one in tab order,
   mark others with aria-hidden="true"
3. If accidental duplication: remove duplicate elements
4. Test with screen reader after fix

Priority: Medium
- Not blocking access to content
- But significantly degrades user experience
- Easy to fix
- Affects every page on the site
```

---

## Резюме по всем трем багам:

**Общая проблема:** Недостаточное внимание к screen reader UX при разработке.

**Паттерн ошибок:**
1. Декоративные элементы не скрыты от screen readers (aria-hidden="true")
2. Дублирование элементов без учета accessibility
3. Skip links не протестированы с реальными screen readers

**Рекомендация для команды разработки:**
- Тестировать с реальными screen readers (NVDA, JAWS, VoiceOver)
- Использовать aria-hidden="true" для декоративных элементов
- Проверять что skip links ведут в правильное место
- Избегать дублирования интерактивных элементов

**Позитивное:**
- Автоматические тесты (axe-core) показали 0 violations
- Базовая структура HTML правильная
- Проблемы легко исправить

**Вывод:**
Сайт технически хорошо сделан, но нуждается в тестировании
с реальными screen readers для выявления UX проблем.

---

*Документ создан: 2026-03-08*
*Тестировщик: Andriy Butenko*
*Инструменты: NVDA 2025.3, Chrome, axe-core 4.11.1*
