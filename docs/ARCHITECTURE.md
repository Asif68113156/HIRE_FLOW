# 1. Problem Statement
Recruitment teams often struggle with scattered data. Moving a candidate through a hiring process requires tracking current status, auditing past movements, and filtering large arrays of humans via complicated conditional factors (e.g., "stuck in a stage," "recently rejected"). Our objective is to construct a scalable tracking pipeline emphasizing data immutability and high-level search accuracy. 

# 2. Product Overview
The Mini Hiring Pipeline is a specialized SaaS dashboard structured around the standard recruiter flow:
`Applied -> Screening -> Interview -> Offer -> Hired`. 
It ensures candidates proceed logically, logs every movement in a read-only audit book, and uses algorithms to allow recruiters to query standard human phrase logic directly in the primary search bar.

# 3. Features
- **Visual Pipeline Board**: See aggregate numbers and click cleanly into detailed candidate profiles.
- **Intelligent Filter & Sub-search**: Capable of cross-referencing natural questions against structural constraints.
- **Immutable Ledger**: View an uneditable history of what happened and when.
- **Automated Metric Timers**: Shows exact durational spans denoting how long a candidate has been in their active stage.

# 4. UI Design
Designed utilizing Bootstrap 5 core structure combined heavily with custom CSS overlays. 
Key aesthetics:
- Glassmorphism navigation wraps enabling modern background diffusion.
- Subtle drop-shadow transitions (lifting effect upon hovering).
- Custom stage-color badging (e.g., Purple for Offers, Amber for Interviews).

# 5. Python Architecture
Follows a modular service-oriented structure:
- **`app.py` & `routes/`**: Handles pure navigation and IO formatting.
- **`services/`**: Thick integration holding logic for CRUD operations and sequence bounding. 
- **`search/`**: Dedicated module isolating semantic regex pulling from the rest of the web layer.

# 6. Database Design
Built around a 1-to-Many SQLAlchemy connection using SQLite:
- `Candidate` (Table): Real-time snapshot of contact details + current stage.
- `StageHistory` (Table): Ledger holding Foreign Key to `Candidate`, logging `from_stage`, `to_stage`, and tz-aware `timestamps`. 

# 7. Stage Transition Logic
An isolated ruleset explicitly tracking Allowed Movements (e.g., Screening -> Interview = Pass / Screening -> Offer = Fail). Banned requests throw custom HTTP 400 violations ensuring the application state never de-syncs.

# 8. Immutable Audit Trail
The history ledger is write-only. Application endpoints do not include `DELETE` or `PUT/PATCH` operations touching the `StageHistory` tables. All updates are handled programmatically through `db.session.add(history)` sequentially behind core Candidate model changes.

# 9. Search Architecture
Implemented dynamically in `search/`:
1. `parser.py`: Breaks down query strings for variables. 
2. `filters.py`: Applies logical WHERE clauses to SQLAlchemy. (e.g., Stage overlaps).
3. `ranking.py`: Compiles results and returns contextual explanations.

# 10. Fuzzy Matching
Implemented via `RapidFuzz`.
- Calculates Levenshtein-based similarity (`fuzz.WRatio`) mapped against dictionary elements. 
- Filters dropped on a `60%` threshold constraint to hide weak similarities while allowing natural typos (e.g., "Sharam" yielding "Priya Sharma").

# 11. Example Search Queries 
Tested successfully via terminal and test beds:
- `"sharam"` (Fuzzy matching target) 
- `"Interview Candidates since Monday"` (Logical cross-referencing)
- `"Screening > 7 days"` (Historical tracking computation)
- `"Who reached offer but didn't get hired"` (Negative sub-query tracking)

# 12. AI Usage
Utilized LLMs for fast boilerplate generation, Bootstrap element combinations, generating initial test fixtures, and compiling baseline regex functions to trim development hours dramatically.

# 13. AI Disagreement
The AI advocated for simple DOM-based locking for form elements to prevent bad stage transitions. This was explicitly overridden. The application enforces logic centrally at `services/transitions.py` using `validate_stage_transition()` before processing database commits, prioritizing server integrity mapping over frontend validation facades.

# 14. Future Improvements
- Migration off of SQLite to PostgreSQL.
- Add Google OAuth logins mapping to Recruiter actors.
- Asynchronous task processing (Celery) parsing uploaded PDF resumes.

# 15. GitHub Repository Link
[Repository would be linked here]
