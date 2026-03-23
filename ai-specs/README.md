# Smart CV Filter - AI Powered Talent Selection

This repository contains an advanced architectural solution designed to automate talent screening using **Google Gemini AI**, ensuring data privacy and selection objectivity through **Spec-Driven Development (SDD)**.

## 🚀 Project Overview
**Smart CV Filter** performs a **Deep Semantic Analysis** to understand a candidate's actual experience, going beyond simple keyword matching. It is built to be portable, highly typed, and AI-compliant.

## 🛡️ Core Pillars
* **Privacy First (GDPR Ready):** Features a **Local Anonymizer** that sanitizes PII (names, emails, phones) locally before any cloud processing.
* **Objective Evaluation (40/30/30 Rubric):** Eliminates AI bias with a strict, deterministic scoring rubric:
    * **40%**: Direct Industry Experience (B2B Sales/Account Executive).
    * **30%**: Communication & Closing skills.
    * **30%**: Tech Market Knowledge.
* **Total Traceability:** Every decision is persisted in a physical **SQL Database** (`smart_cv.db`) for post-analysis auditing.
* **AI Managed Standards:** Follows strict rules defined in `ai-specs/` to ensure consistent, high-quality code across different AI Copilots (Gemini, Claude, Cursor).

## 📁 Repository Structure
```text
.
├── ai-specs/                # AI Agent rules & development standards
├── src/
│   ├── backend/             # Core logic (Extractor, Anonymizer, Analyzer)
│   │   ├── inputs/          # CV Ingestion (PDF, DOCX, TXT)
│   │   └── output/          # Classified CVs (RECLUTADOS/DESCARTADOS)
│   └── data/                # SQL Persistence (smart_cv.db)
├── DEVELOPMENT_LOG.md       # Technical bitacora & Bug fixes
└── HISTORY_AND_ROADMAP.md   # Functional milestones & Future vision
```

## 🛠️ Usage: Command-Based Workflow
This project follows the OPSX Workflow defined in our AI Specifications:
* Explore: /opsx:explore [Task] to analyze impact.

* Plan: /opsx:propose [Feature] to create an implementation plan in ai-specs/changes/.

* Execute: /opsx:apply [Plan] to implement code using TDD and Type Safety.

* Archive: /opsx:archive to verify the Definition of Done (DoD) and update logs.