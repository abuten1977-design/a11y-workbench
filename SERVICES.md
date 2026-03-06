# 💼 SERVICES: A11y Workbench

**Версія:** 1.0  
**Дата:** 6 березня 2026

---

## 🎯 ПРОДАВАЄМІ ПОСЛУГИ

**Позиціонування:** Manual screen reader accessibility testing by real blind expert

---

## 📦 ПАКЕТИ ПОСЛУГ

### 1. Quick Blind Check

**Опис:** Швидка перевірка 1 сторінки або компонента

**Що включено:**
- Тестування з NVDA
- 5-10 основних замечань
- Короткий summary
- Пріоритети (critical/serious/moderate)

**Deliverable:**
- Markdown звіт
- Список issues з severity
- Рекомендації

**Час:** 30-60 хвилин  
**Ціна:** $50-100

**Підходить для:**
- Швидка перевірка перед релізом
- Перевірка одного компонента
- Proof of concept

---

### 2. Screen Reader Smoke Test

**Опис:** Перевірка критичного user flow

**Що включено:**
- Тестування ключового шляху (login, checkout, form)
- Детальні issue reports
- WCAG criteria mapping
- Screen reader output evidence
- Remediation recommendations

**Deliverable:**
- Developer-ready issue reports
- Evidence (screen reader output)
- WCAG compliance notes
- Priority fixes list

**Час:** 1-2 години  
**Ціна:** $100-200

**Підходить для:**
- Checkout flow
- Login/signup
- Critical forms
- Main navigation

---

### 3. Accessibility Bug Report Pack

**Опис:** Повний аудит сторінки або розділу

**Що включено:**
- Детальне тестування з NVDA
- Structured issue reports (10-30 issues)
- WCAG 2.2 AA assessment
- Evidence для кожного issue
- Remediation recommendations
- Priority roadmap

**Deliverable:**
- Client summary report
- Developer issue list (Markdown/JSON/CSV)
- WCAG criteria referenced
- Severity breakdown
- Recommended next steps

**Час:** 3-5 годин  
**Ціна:** $300-500

**Підходить для:**
- Homepage audit
- Full page review
- Section audit (e.g., all forms)
- Pre-launch review

---

### 4. Retest Service

**Опис:** Перевірка виправлених issues

**Що включено:**
- Retest всіх reported issues
- Confirmation або нові знахідки
- Updated status
- Retest notes

**Deliverable:**
- Retest report
- Pass/fail для кожного issue
- New issues (якщо є)

**Час:** 30 хвилин - 2 години  
**Ціна:** $50-150 (залежить від кількості issues)

**Підходить для:**
- Після фіксів
- Verification перед релізом
- Iterative improvement

---

## 🎨 CUSTOM PACKAGES

### Full Website Audit

**Опис:** Комплексний аудит всього сайту

**Що включено:**
- Multiple pages/flows
- Comprehensive issue list
- WCAG compliance report
- Priority roadmap
- Follow-up consultation

**Ціна:** Custom (від $1000)

---

### Ongoing Accessibility Support

**Опис:** Регулярна підтримка

**Що включено:**
- Monthly retests
- New feature reviews
- Consultation
- Priority support

**Ціна:** Custom (від $500/місяць)

---

## 📋 DELIVERABLE FORMATS

### Developer Report (Markdown)

```markdown
# Accessibility Issues: Project Name

## Summary
- Total issues: 15
- Critical: 2
- Serious: 5
- Moderate: 6
- Minor: 2

## Issues

### Issue #1: Unlabeled Submit Button
**Severity:** Serious  
**WCAG:** 4.1.2 Name, Role, Value (Level A)  
**Affected Element:** `.checkout-form button[type=submit]`

**Steps to Reproduce:**
1. Navigate to checkout page
2. Tab to submit button
3. Listen to NVDA announcement

**Observed Behavior:**
NVDA announces "button" without any label

**Expected Behavior:**
NVDA should announce "Submit order, button"

**User Impact:**
Blind users cannot identify button purpose

**Evidence:**
```
NVDA output: "button"
```

**Suggested Fix:**
Add `aria-label="Submit order"` or visible text inside button

---
```

### Client Summary (Markdown)

```markdown
# Accessibility Audit Summary: Project Name

**Date:** March 6, 2026  
**Tester:** [Your Name]  
**Assistive Technology:** NVDA 2024.1  
**Browser:** Chrome 120

## Executive Summary

Tested checkout flow with NVDA screen reader. Found 15 accessibility issues, including 2 critical blockers that prevent blind users from completing purchase.

## Findings by Severity

- **Critical (2):** Block task completion
- **Serious (5):** Significant barriers
- **Moderate (6):** Usability issues
- **Minor (2):** Minor improvements

## WCAG Criteria Referenced

Issues found related to:
- 4.1.2 Name, Role, Value (5 issues)
- 2.1.1 Keyboard (3 issues)
- 1.3.1 Info and Relationships (4 issues)
- 2.4.3 Focus Order (2 issues)
- 3.3.2 Labels or Instructions (1 issue)

## Key Blockers

1. **Unlabeled submit button** - Users cannot complete checkout
2. **Keyboard trap in modal** - Users cannot close payment dialog

## Recommended Next Steps

1. Fix critical issues (2 issues) - Priority 1
2. Fix serious issues (5 issues) - Priority 2
3. Schedule retest after fixes
4. Address moderate/minor issues in next sprint

## Detailed Issues

See attached developer report for full details.
```

### JSON Export

```json
{
  "project": {
    "name": "Project Name",
    "tested_at": "2026-03-06T10:00:00Z",
    "tester": "Your Name",
    "assistive_tech": "NVDA",
    "browser": "Chrome"
  },
  "summary": {
    "total_issues": 15,
    "critical": 2,
    "serious": 5,
    "moderate": 6,
    "minor": 2
  },
  "issues": [
    {
      "id": "issue_1",
      "title": "Unlabeled Submit Button",
      "severity": "serious",
      "wcag": "4.1.2",
      "affected_element": ".checkout-form button[type=submit]",
      "description": "...",
      "steps": "...",
      "observed": "...",
      "expected": "...",
      "impact": "...",
      "fix": "...",
      "evidence": ["NVDA: button"]
    }
  ]
}
```

---

## 💰 PRICING STRATEGY

### Factors:
- Complexity (simple page vs complex flow)
- Number of issues expected
- Urgency (rush jobs +50%)
- Retest discount (-30%)

### Hourly Rate Equivalent:
- Target: $50-100/год
- Competitive with Fable ($100-150/год)
- But fixed price packages (easier to sell)

---

## 🎯 TARGET CLIENTS

### Ideal Clients:
1. **Startups** - need quick compliance check
2. **E-commerce** - checkout flows critical
3. **SaaS companies** - forms and dashboards
4. **Agencies** - outsource accessibility testing
5. **Enterprise** - ongoing support

### Where to Find:
- UserTesting platform
- Upwork/Fiverr
- LinkedIn outreach
- Direct contact (cold email)
- Referrals

---

## 📊 VALUE PROPOSITION

**Why choose me:**

1. **Real blind user** - not automated tools
2. **NVDA expert** - most popular free screen reader
3. **Deque trained** - professional methodology
4. **Fast turnaround** - 24-48 hours
5. **Developer-ready reports** - actionable fixes
6. **AI-assisted workflow** - efficient but human-verified
7. **Competitive pricing** - $50-500 vs $100-150/hr

---

## 🚀 SALES PROCESS

### 1. Discovery Call (15 min)
- Understand needs
- Explain process
- Recommend package

### 2. Proposal
- Package description
- Deliverables
- Timeline
- Price

### 3. Agreement
- Simple contract
- Payment terms (50% upfront)
- NDA if needed

### 4. Testing
- Access to staging/demo
- Testing with NVDA
- Issue documentation

### 5. Delivery
- Send reports
- Brief walkthrough call
- Answer questions

### 6. Retest (optional)
- After fixes
- Verification
- Final sign-off

---

## 📝 SAMPLE PROPOSALS

### Quick Check Proposal

```
Subject: Accessibility Quick Check - $75

Hi [Client],

I can provide a quick accessibility check of your [page/component] using NVDA screen reader.

What you'll get:
- 30-minute NVDA testing session
- 5-10 key findings
- Priority recommendations
- Markdown report

Timeline: 24 hours
Price: $75

This is perfect for a quick pre-launch check or single component review.

Interested? Let me know and I'll send a simple agreement.

Best,
[Your Name]
Blind Accessibility Tester | NVDA Expert
```

### Full Audit Proposal

```
Subject: Checkout Flow Accessibility Audit - $350

Hi [Client],

I can provide a comprehensive accessibility audit of your checkout flow using NVDA screen reader.

What you'll get:
- Complete NVDA testing of checkout process
- 15-30 detailed issue reports
- WCAG 2.2 AA compliance assessment
- Developer-ready fixes
- Client summary report
- 30-min walkthrough call

Timeline: 3-5 business days
Price: $350

Includes one free retest after fixes.

This ensures your checkout is accessible to blind users and WCAG compliant.

Interested? I can start this week.

Best,
[Your Name]
Blind Accessibility Tester | Deque Trained
```

---

## 🎓 PROOF OF EXPERTISE

**Portfolio pieces:**
- Sample reports (anonymized)
- Statistics (projects tested, issues found)
- Testimonials (after first clients)
- Certifications (Deque)
- Tools (A11y Workbench - custom system)

**LinkedIn headline:**
"Blind Accessibility Tester | NVDA Expert | WCAG 2.2 Specialist | Helping companies build inclusive digital experiences"

---

## 📈 GROWTH STRATEGY

### Month 1-2:
- 3-5 sample projects (portfolio)
- Register on UserTesting
- LinkedIn profile
- First paid clients

### Month 3-4:
- 10+ completed projects
- Testimonials
- Referrals
- Upwork/Fiverr presence

### Month 6+:
- Regular clients
- Ongoing contracts
- Possible job offers
- Scale (maybe)

---

**Останнє оновлення:** 6 березня 2026, 18:30 CET  
**Версія:** 1.0  
**Статус:** Ready to sell
