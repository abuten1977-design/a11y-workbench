# Accessibility Report: https://lifeindenmark.borger.dk/

**Generated:** 2026-03-08 17:21
**Project:** https://lifeindenmark.borger.dk/

## Summary

- **Total Issues:** 3
- **Critical:** 0
- **Serious:** 2
- **Moderate:** 1
- **Minor:** 0

## Serious Issues (2)

### 1. Skip to main content link targets incorrect location with unlabeled images

**WCAG:** 2.4.1
**Status:** new

**Steps to Reproduce:**
1. Navigate to https://lifeindenmark.borger.dk/
2. Press Tab to reach "Skip to main content" link
3. Activate the link (press Enter)
4. Listen to NVDA announcements
5. Observe focus lands on unlabeled images instead of main content
```


**Observed Behavior:**
When "Skip to main content" link is activated, focus moves to a location where NVDA announces "No description" for multiple images. The skip link does not bypass the header navigation as intended. Users still encounter problematic elements before reaching actual page content.
```


**Expected Behavior:**
Skip link should move focus directly to the beginning of the main page content, bypassing all header navigation, logos, and decorative elements. Focus should land on the first heading or content element in the main landmark.
```


**User Impact:**
Screen reader and keyboard users cannot efficiently bypass navigation. The skip link, which is meant to improve accessibility, actually leads users to inaccessible content (unlabeled images). This defeats the purpose of the skip link and creates a poor user experience.
```


**Suggested Fix:**
1. Verify the #main anchor is placed at the correct location (start of main content, not in header)
2. Ensure #main is on the <main> element or first content heading
3. Remove or properly hide decorative images that appear before main content


**Evidence:**
- *note:* This is a SERIOUS issue because:

1. Defeats the purpose of skip link - users still have to navigate through obstacles
2. Unlabeled images create confusion ("What am I looking at?")
3. Violates WCAG 2.4.1 Bypass Blocks - the bypass mechanism does not work properly
4. Affects ALL screen reader users on EVERY page visit

Impact: Keyboard users waste time, screen reader users get confused by unlabeled graphics, users may think the skip link is broken.

Recommendation: Move #main anchor to AFTER decorative images, or mark images as aria-hidden="true"
- *code:* <!-- Current implementation (WRONG): -->
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
  <img src="..." alt="">  <!-- Hidden from screen readers -->
</div>

<main id="main">
  <h1>The official guide to life in Denmark</h1>
  <!-- Main content starts here -->
</main>
- *screen_reader_output:* NVDA output when using skip link:

1. Focus on "Skip to main content" link at top of page
2. Press Enter to activate
3. NVDA announces: "Нет описания, graphic" (3 times in a row)
4. Focus lands on unlabeled images instead of main content

Expected: Focus should move directly to main content area
Actual: Focus moves to unlabeled images

Testing: NVDA 2025.3, Chrome, Windows 11, 2026-03-08

---

### 2. Topic category icons missing alternative text - links unusable for screen readers

**WCAG:** 1.1.1
**Status:** new

**Steps to Reproduce:**
1. Navigate to https://lifeindenmark.borger.dk/
2. Scroll to "All topics" section
3. Use screen reader (NVDA) to navigate topic category links
4. Links announce as "No description" or only URL
```


**Observed Behavior:**
Topic category links (Settle in Denmark, Housing and Moving, Working, etc.) contain decorative icon images with empty alt text (alt=""). When these icons are the only or primary content in a link, screen readers announce "No description" or just the link URL, making the links unusable.
```


**Expected Behavior:**
Either:
- Icons should have descriptive alt text matching the link purpose (e.g., alt="Settle in Denmark"), OR
- Icons should be marked aria-hidden="true" and link should have visible text or aria-label
```


**User Impact:**
Screen reader users cannot understand the purpose of these links, making major site sections inaccessible. Users cannot navigate to important content areas like Housing, Working, Family sections. This is a critical barrier to using the site.
```


**Suggested Fix:**
Option 1: Add descriptive alt text to icons
<img src="icon.svg" alt="Settle in Denmark">

Option 2: Hide icons and add text labels
<a href="/settle-in-denmark">
  <img src="icon.svg" alt="" aria-hidden="true">
  <span>Settle in Denmark</span>
</a>

Option 3: Use aria-label on link
<a href="/settle-in-denmark" aria-label="Settle in Denmark">
  <img src="icon.svg" alt="" aria-hidden="true">
</a>


**Evidence:**
- *note:* This is a SERIOUS issue because:

1. Affects 12 major navigation links (all topic categories)
2. Creates confusing user experience - "No description" after every link
3. Violates WCAG 1.1.1 - decorative images not properly marked
4. Makes site sound unprofessional and poorly implemented

Impact: Confusion ("What is No description? Is something broken?"), annoyance (extra announcement after every link), inefficiency (takes longer to navigate)

Why this happens: Developers used alt="" thinking it would hide the image, but forgot to add aria-hidden="true". Screen readers still detect the image and announce it as "No description".

Recommendation: Add aria-hidden="true" to all decorative icons in links. Simple fix that will improve UX significantly.
- *code:* <!-- Current implementation (WRONG): -->
<a href="/settle-in-denmark">
  <img src="/-/media/spritemaps/EmnerSpritemap.svg#Udlaendige_i_danmark" alt="">
  Settle in Denmark
</a>

<!-- Problem: alt="" without aria-hidden="true" -->
<!-- Screen readers announce the empty alt as "No description" -->

<!-- Correct implementation (Recommended): -->
<a href="/settle-in-denmark">
  <img src="/-/media/spritemaps/EmnerSpritemap.svg#Udlaendige_i_danmark" 
       alt="" 
       aria-hidden="true">
  Settle in Denmark
</a>
- *screen_reader_output:* NVDA output when navigating topic category links:

"Settle in Denmark, link, Нет описания, graphic"
"Housing and moving, link, Нет описания, graphic"
"Working, link, Нет описания, graphic"
"Family and children, link, Нет описания, graphic"

Pattern: Each topic link contains text label (good) + decorative icon with alt="" (causes "Нет описания" announcement)

Expected: Icons should be marked aria-hidden="true" to prevent announcement
Actual: Icons have empty alt="" but are NOT marked aria-hidden, causing NVDA to announce "Нет описания" (No description)

Testing: NVDA 2025.3 (Russian), Chrome, Windows 11, 2026-03-08

---

## Moderate Issues (1)

### 1. Duplicate logo images in header - announced 4 times by screen reader

**WCAG:** 2.4.4
**Status:** new

**Steps to Reproduce:**
1. Navigate to https://lifeindenmark.borger.dk/
2. Use screen reader (NVDA) to navigate from top of page
3. After "Skip to main content" link, tab through header
4. Observe 4 identical "Life in Denmark logo" announcements


**Observed Behavior:**
Logo image appears 4 times with identical alt="Life in Denmark logo". NVDA announces "Life in Denmark logo, link" 4 times consecutively. All 4 logos link to the same homepage URL.


**Expected Behavior:**
Logo should appear once in the header with appropriate alt text. Additional logo instances (if needed for responsive design) should be marked with aria-hidden="true" to prevent redundant announcements.
```


**User Impact:**
Screen reader users experience confusion and frustration. Wastes time navigating through redundant links. Makes header navigation inefficient. Users may think they are stuck or that the page has an error.
```


**Suggested Fix:**
Option 1: Keep only one logo visible, hide others with aria-hidden="true"
Option 2: Use CSS to show/hide logos for different screen sizes, mark hidden ones with aria-hidden="true"
Option 3: Remove duplicate logo elements entirely



**Evidence:**
- *note:* This is a SERIOUS issue because:

1. Defeats the purpose of skip link - users still have to navigate through obstacles
2. Unlabeled images create confusion ("What am I looking at?")
3. Violates WCAG 2.4.1 Bypass Blocks - the bypass mechanism doesn't work properly
4. Affects ALL screen reader users on EVERY page visit

- *code:* ```html
<!-- Current implementation (WRONG): -->
<a href="#main">Skip to main content</a>

<!-- The #main anchor is placed BEFORE the unlabeled images -->
<div id="main">
  <img src="..." alt="">  <!-- Unlabeled image 1 -->
  <img src="..." alt="">  <!-- Unlabeled image 2 -->
  <img src="..." alt="">  <!-- Unlabeled image 3 -->
  <!-- Actual content starts here -->
</div>

- *screen_reader_output:* NVDA output when using skip link:

1. Focus on "Skip to main content" link at top of page
2. Press Enter to activate
3. NVDA announces: not discribed , graphic" (3 times in a row)
4. Focus lands on unlabeled images instead of main content


---
