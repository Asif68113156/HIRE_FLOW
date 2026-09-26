# Mini Hiring Pipeline

## Overview 
Mini Hiring Pipeline is a production-ready, SaaS-like web application designed for recruiters to efficiently manage a candidate pipeline for a single job opening. The application demonstrates complex backend logic, including strict sequence validations, an immutable audit trail, and a powerful natural language search engine powered by fuzzy string matching.

## Features
- **Strict Pipeline Sequencing**: Candidates move through an allowed flow (`Applied → Screening → Interview → Offer → Hired`) and invalid transitions (e.g., `Applied → Interview` or moving backwards) are blocked securely on the server side.
- **Immutable Audit Trail**: Every stage change generates an uneditable history log.
- **Dynamic Analysis**: Automatically calculates how long a candidate has been sitting in their current pipeline stage.
- **Intelligent Search**: Interpret natural language search queries such as `"stuck in screening > 7 days"` or `"who reached offer but didn't get hired"`, combined with fuzzy string matching.
- **Premium UI**: Provides a clean, modern aesthetic utilizing custom constraints alongside Bootstrap 5, featuring micro-animations, glassmorphism, and responsive drag-and-drop-style dashboard cards.

## Tech Stack
- **Backend Language**: Python 3.11+
- **Core Framework**: Flask
- **ORM & Database**: SQLAlchemy / SQLite
- **Fuzzy Matching Logic**: RapidFuzz
- **Templating**: Jinja2
- **Frontend / Styling**: HTML5, Vanilla JavaScript, Bootstrap 5 + Custom CSS
- **Testing**: pytest

## Architecture
The application separates concerns strictly:
1. **Routing Layer**: Flask controllers (`app.py`, `routes/`).
2. **Service Layer**: Pure Python business logic extracting data complexity (`services/candidate_service.py`, `services/transitions.py`).
3. **Data Model**: SQLAlchemy models outlining the schema and relations (`models/candidate.py`, `models/history.py`).
4. **Custom NLP Engine**: Specialized sub-pipeline taking unstructured requests, generating DB filters, and appending fuzzy matches (`search/`). 

## Database Design
- `Candidate`: The root entity tracking the individual's generic profile data and their `current_stage`.
- `StageHistory`: A write-only immutable ledger that references a Candidate (`candidate_id`). Tracks the `from_stage`, `to_stage`, `actor`, and the accurate `timestamp`.

## Stage Transition Rules
The frontend may prevent bad clicks, but security happens server-side via `validate_stage_transition()`.
Transitions are validated server-side. For a production recruiting application, frontend states can be tampered with manually or desync with concurrent actions. Implementing strict server-side logic ensures the integrity of the audit ledger cannot be compromised by API calls. 

## Search Design
The Search Module operates in a tiered execution flow:
- **Query Parser**: Uses Regex logic heavily targeting specific syntax hooks to pull variables like "since", "days", and "stage".
- **Filtering**: Converts parser definitions into SQLAlchemy ORM constraints to execute DB-level cuts for speed.
- **Fuzzy Matching**: Re-evaluates what is remaining in the `query` text utilizing `rapidfuzz` against Candidate names to fix spelling mistakes gracefully.
- **Ranking**: Calculates composite scores prioritizing direct matches mixed with the fuzzy algorithm scoring limits.
- **Invalid-Query Handling**: Communicates to the user exactly what parameters were detected, and guides them if the query was confusing. 

## How to Run
Follow these commands verbatim in your terminal:

```bash
# Verify you are in the project root directory

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# Windows:
venv\Scripts\activate
# (For Mac/Linux use: source venv/bin/activate)

# 3. Install packages
pip install -r requirements.txt

# 4. Initialize Database and Seed Demo users
python seed.py

# 5. Start the Web Server
python app.py
```

Then open `http://127.0.0.1:5000` in your web browser.

## Testing
```bash
pytest 
``` 

## Design Decisions
1. **Server-Side Render vs SPA**: Opted for Jinja2 + Flask route delivery rather than building a detached API/React layer, sticking precisely to the assessment request to utilize strict Python outputs. 
2. **RapidFuzz vs Basic SQL ILIKE**: Enabled complex typo resolution (e.g., retrieving `Priya Sharma` when a user types `sharam`).
3. **Time Analysis vs CRON Check**: Opted to run date deltas in real-time during Jinja rendering or API execution via Python `dateutil` to guarantee live-accurate "Time in Stage" metrics without requiring background daemon services.

## What I Would Build With More Time
- **Authentication & RBAC**: Real `actor` extraction mapping out which recruiter caused which status change.
- **PostgreSQL Migration**: Upgrading the single SQLite file to handle concurrency tracking across multiple large recruiting groups.
- **Resume Parsing Engine**: Using standard libraries to automatically auto-fill form inputs upon uploading a candidate's PDF resume.
- **Email Notification Event Loop**: Automatically notify candidates dynamically as they process through the pipeline states.
