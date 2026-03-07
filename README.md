# A11y Workbench

**Accessibility testing workflow system for blind accessibility specialists**

A production-ready system for manual accessibility testing with AI-assisted reporting, designed by and for blind screen reader users.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

A11y Workbench is a personal production system for accessibility testing that helps blind specialists:
- Quickly capture accessibility issues during manual testing
- Transform short notes into professional defect reports
- Manage projects and testing sessions
- Export developer-ready reports
- Build portfolio of accessibility work

### Key Innovation
Built by a blind accessibility specialist for real-world accessibility testing workflow, with full keyboard navigation and screen reader support.

---

## ✨ Features

### 🔍 Testing Workflow
- **Project management** - Organize work by clients/projects
- **Target tracking** - Pages, flows, forms, components
- **Test sessions** - Track what was tested, when, and with which tools
- **Quick capture** - Fast issue logging during testing
- **Structured reports** - Professional defect documentation

### 📋 Issue Management
- **WCAG mapping** - Link issues to WCAG 2.2 criteria
- **Severity levels** - Critical, serious, moderate, minor
- **Status tracking** - New → Reported → Fixed → Retested
- **Evidence support** - Screen reader output, code snippets, notes

### 📊 Reporting & Export
- **Developer reports** - Structured issue lists with reproduction steps
- **Client summaries** - Executive-level findings overview
- **Multiple formats** - Markdown, JSON, CSV
- **Portfolio mode** - Anonymized sample reports

### ♿ Accessibility First
- **Keyboard-first interface** - Full keyboard navigation
- **Screen reader optimized** - Tested with NVDA and VoiceOver
- **Logical structure** - Proper headings and landmarks
- **No inaccessible modals** - Everything accessible

### 🤖 AI-Assisted (Optional)
- Transform quick notes into structured reports
- Suggest issue categories and WCAG criteria
- Maintain human verification and control

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- SQLite3
- (Optional) Google Cloud account for deployment

### Installation

```bash
# Clone repository
git clone https://github.com/abuten1977-design/a11y-workbench.git
cd a11y-workbench

# Install dependencies
pip install -r requirements.txt

# Initialize database
python migrate.py

# Run server
python api_server_v2.py
```

### Access Dashboard
```
http://localhost:8000
```

---

## 📖 Documentation

- [Architecture](ARCHITECTURE.md) - System design and components
- [Data Model](DATA_MODEL.md) - Database schema and entities
- [Roadmap](ROADMAP.md) - Development plan and phases
- [Services](SERVICES.md) - Offered accessibility testing services
- [Career Strategy](CAREER_STRATEGY.md) - How this supports accessibility career

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.8+
- **Database:** SQLite3
- **Frontend:** HTML5, vanilla JavaScript (accessibility-first)
- **Deployment:** Google Cloud Platform (optional)
- **AI Integration:** Google Gemini API (optional)

---

## 💼 Use Cases

### For Accessibility Specialists
- Manage multiple client projects
- Track testing progress
- Generate professional reports
- Build portfolio of work

### For Freelancers
- Quick accessibility reviews
- WCAG compliance audits
- Retest verification
- Client deliverables

### For Job Seekers
- Demonstrate professional workflow
- Show systematic approach
- Provide sample reports
- Prove technical skills

---

## 🎓 Background

Created by a blind accessibility specialist with:
- 7 years teaching blind users digital technologies
- Experience with WCAG testing and reporting
- Real-world screen reader expertise (NVDA, VoiceOver, JAWS)
- Understanding of accessibility testing challenges

---

## 📋 Project Status

**Current Phase:** Phase 2 - Issue Workflow  
**Status:** Active Development  
**Version:** 0.2.0 (Beta)

See [ROADMAP.md](ROADMAP.md) for detailed progress.

---

## 🤝 Contributing

This is currently a personal production tool, but feedback and suggestions are welcome!

---

## 📧 Contact

**Andriy Butenko**  
Blind Accessibility & Assistive Technology Specialist  
📧 abuten1977@gmail.com  
🇩🇰 Copenhagen, Denmark

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🌟 Related Projects

- [AudioTrace AI](https://github.com/abuten1977-design/audiotrace-ai) - Audio code maps for blind developers
- RHVoice Tools - Speech synthesis integration tools

---

*"Accessibility testing by someone who actually uses screen readers every day"*
