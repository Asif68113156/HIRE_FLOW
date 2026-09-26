# Mini Hiring Pipeline — System Architecture & Design Document

**GitHub Repository:** [https://github.com/Asif68113156/HIRE_FLOW](https://github.com/Asif68113156/HIRE_FLOW)  
**Author:** Asif Siddiqui  
**Project:** Mini Hiring Pipeline (Technical Assessment)  
**Tech Stack:** Python 3.11+, Flask, SQLAlchemy, SQLite, RapidFuzz, Bootstrap 5, Jinja2, pytest

---

## 1. Executive Summary & Problem Statement

Recruitment teams frequently struggle with fragmented data, manual stage updates, and rigid search interfaces. Candidate tracking requires:
1. Enforcing strict, sequential hiring stages (`Applied → Screening → Interview → Offer → Hired`).
2. Maintaining an **immutable audit trail** of all state transitions for compliance.
3. Enabling recruiters to query candidates using **natural language** and tolerant **fuzzy matching** rather than exact field lookups.

The **Mini Hiring Pipeline** is a production-ready, SaaS-grade web application built to solve these challenges with server-side validation, sub-millisecond query parsing, and an enterprise glassmorphism recruiter dashboard.

---

## 2. Product & Technical Architecture

The application follows a clean 3-tier modular architecture separating presentation, business logic, data modeling, and search parsing:

```
                  ┌────────────────────────────────────────┐
                  │          Flask Presentation Layer      │
                  │   (routes/candidates.py, search.py)    │
                  └───────────────────┬────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │          Service / Business Layer       │
                 │   (services/candidate_service.py,       │
                 │    services/transitions.py)             │
                 └──────────┬──────────────────┬───────────┘
                            │                  │
 ┌──────────────────────────┴──┐    ┌──────────┴────────────────────────┐
 │   Database / ORM Layer      │    │     NLP & Fuzzy Search Module     │
 │  (models/candidate.py,      │    │   (search/parser.py, filters.py,  │
 │   models/history.py)        │    │    search/fuzzy.py, ranking.py)   │
 └─────────────────────────────┘    └───────────────────────────────────┘
```

---

## 3. Database Schema & Data Models

### 3.1 Candidate Model (`candidates` table)
- `id` (Integer, Primary Key)
- `name` (String 100, Mandatory)
- `email` (String 120, Unique, Mandatory)
- `phone` (String 20, Mandatory)
- `role` (String 100, Mandatory)
- `resume_url` (String 255, Mandatory PDF path)
- `notes` (Text, Mandatory)
- `current_stage` (String 50, Default: `'Applied'`)
- `created_at` / `updated_at` (DateTime, UTC)

### 3.2 Immutable Audit Ledger (`stage_history` table)
- `id` (Integer, Primary Key)
- `candidate_id` (Integer, Foreign Key → `candidates.id`)
- `from_stage` (String 50, Nullable for initial creation)
- `to_stage` (String 50, Mandatory)
- `timestamp` (DateTime, UTC, Auto-generated)
- `actor` (String 100, Default: `'Recruiter'`)

> **Immutability Guarantee:** The `StageHistory` model is strictly append-only. There are no `UPDATE` or `DELETE` endpoints for history logs in the application.

---

## 4. Business Logic & Server-Side Transition Validation

Stage progression follows a deterministic state machine:

$$\text{Applied} \longrightarrow \text{Screening} \longrightarrow \text{Interview} \longrightarrow \text{Offer} \longrightarrow \text{Hired}$$

- Candidates may be moved to **`Rejected`** from any active stage prior to `Hired`.
- Candidates in terminal stages (`Hired`, `Rejected`) cannot be moved.
- **Server-Side Enforcement:** Validation is executed centrally in `services/transitions.py` using `validate_stage_transition()`. Invalid state skips (e.g. `Applied → Offer`) trigger an `InvalidTransitionError` returning HTTP 400 Bad Request.

---

## 5. Natural Language & Fuzzy Search Engine

The custom search engine operates in a multi-stage execution pipeline without relying on slow external LLM APIs:

1. **Query Parser (`search/parser.py`)**: Uses regular expressions to extract structured intent:
   - **Stage Filters**: `Interview candidates` $\rightarrow$ `stage: 'Interview'`
   - **Time in Stage**: `Screening > 7 days` $\rightarrow$ `min_days: 7`
   - **Date Relativity**: `Moved since Monday` $\rightarrow$ `moved_since: 'monday'`
   - **Boolean Constraints**: `Offer but not Hired` $\rightarrow$ `reached_offer_not_hired: True`
   - **Exclusions**: `everyone except rejected` $\rightarrow$ `exclude_rejected: True`
2. **Database Filter (`search/filters.py`)**: Translates parsed intent into optimized SQLAlchemy ORM queries.
3. **Fuzzy String Matcher (`search/fuzzy.py`)**: Runs `RapidFuzz` Levenshtein similarity (`fuzz.WRatio`) on remaining search terms to handle typos (e.g., `"sharam"` $\rightarrow$ `"Priya Sharma"`).
4. **Fallback Explanation UI**: Displays a clear "Query Understanding" panel if a query cannot be parsed.

---

## 6. AI Interaction & Key Senior Engineering Disagreement

### The Disagreement: Backend State Machine vs. Naive Frontend Locking
- **What the AI Suggested:** Disabling dropdown choices in the HTML frontend interface to prevent recruiters from selecting out-of-order stages.
- **Why I Disagreed & Changed It:** Client-side locking is purely a visual aid, not security. Any user or external script could bypass the frontend by sending a direct `POST` payload to `/candidate/1/stage`. I implemented strict backend validation in `services/transitions.py` to ensure that data integrity is guaranteed at the service layer before any database commit takes place.

---

## 7. Verified Demo Queries & Test Coverage

All 12 unit/integration tests pass in `pytest` (`0.08s`). Verified search behavior:

| Query | Extracted Intent | Results Returned |
|---|---|---|
| `sharam` | Fuzzy Name Match | Priya Sharma |
| `Interview candidates` | Stage: Interview | 4 candidates |
| `Screening > 7 days` | Time > 7 days in Screening | Aisha Khan, Kiran Patel, Zara Sheikh |
| `who reached offer but not hired` | Reached Offer $\land$ $\neg$Hired | Arjun Mehta, Vikram Singh, Nikhil Bose |
| `everyone except rejected` | $\neg$Rejected | 13 candidates |
| `Monday` | Moved since last Monday | 12 candidates |

---

## 8. Future Roadmap & Enhancements

1. **PostgreSQL & Redis Scaling**: Upgrade SQLite to PostgreSQL with Connection Pooling and Celery background workers.
2. **Automated Resume Parsing**: Integrate `PyMuPDF` / `pdfminer` to extract candidate details directly from uploaded PDF files.
3. **Role-Based Access Control (RBAC)**: Implement multi-tenant recruiter authentication with fine-grained action auditing.

---

**GitHub Repository:** [https://github.com/Asif68113156/HIRE_FLOW](https://github.com/Asif68113156/HIRE_FLOW)
