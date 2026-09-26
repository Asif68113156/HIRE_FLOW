# Professional Video Recording & Presentation Guide

This guide provides a professional script and step-by-step walkthrough to present the **Mini Hiring Pipeline** application during your video assessment recording.

---

## 🎙️ Professional Voice Tone & Pacing Tips
1. **Tone**: Confident, articulate, and technical yet clear.
2. **Pacing**: Speak at a steady pace. Pause slightly when highlighting major features (e.g., Server-Side Validation, RapidFuzz engine, Immutable Ledger).
3. **Screen Setup**: Keep the web browser open on `http://127.0.0.1:5000` alongside a clean terminal window for running `pytest`.

---

## 🎬 Section-by-Section Video Script

### **Beat 1: Professional Opening & Tech Stack (0:00 - 1:30)**

**What to show on screen:**
- Open browser at `http://127.0.0.1:5000` showing the Recruiter Dashboard.

**What to say:**
> *"Hello everyone. Today I am presenting the **Mini Hiring Pipeline**, a web-based candidate management platform built strictly using **Python, Flask, SQLAlchemy, SQLite, and RapidFuzz**.*
>
> *This application is designed specifically for technical recruiters to manage job requisitions with strict data integrity, real-time stage tracking, an immutable audit log, and an advanced natural language search engine."*

---

### **Beat 2: Candidate Management & Mandatory PDF Upload (1:30 - 3:00)**

**What to show on screen:**
1. Click the **"Add Candidate"** button.
2. Highlight the red asterisks (`*`) on all fields.
3. Show that trying to submit without a PDF resume or notes triggers validation errors.
4. Fill in:
   - Full Name: `Ananya Verma`
   - Email: `ananya@example.com`
   - Phone: `+91 9876543210`
   - Role: `Software Engineer`
   - Resume: Upload a `.pdf` file
   - Notes: `Strong backend problem solver with 3 years experience.`
5. Click **"Add Candidate to Pipeline"**. Show the new card appearing in `Applied`.

**What to say:**
> *"First, let's look at candidate ingestion. All fields—including Full Name, Email, Phone, Role, Resume PDF, and Notes—are strictly mandatory both on the frontend and on the backend server.
>
> Notice that the system enforces PDF document uploads for resumes instead of plain text URLs. When I submit this valid profile, the candidate is added to the **Applied** column, and an initial audit record is generated."*

---

### **Beat 3: Strict Server-Side Stage Transition Validation (3:00 - 5:00)**

**What to show on screen:**
1. Click on candidate `Rohan Desai` (currently in `Applied`).
2. Show the dropdown menu: Notice that `Interview`, `Offer`, and `Hired` are disabled because the valid order is `Applied → Screening → Interview → Offer → Hired`.
3. Select `Screening` and click **"Execute Move"**. Show the stage update to `Screening`.

**What to say:**
> *"One of the core architectural requirements of this project is strict stage transition validation. The hiring pipeline follows a deterministic state machine: candidates move from **Applied → Screening → Interview → Offer → Hired**, or can be **Rejected** at any point prior to Hired.
>
> Crucially, this validation is enforced **server-side** in `services/transitions.py`. If someone attempts to bypass the UI and post an invalid transition like skipping from `Applied` directly to `Offer`, the server rejects the request with an HTTP 400 error."*

---

### **Beat 4: Dynamic Stage Duration & Immutable Audit Ledger (5:00 - 7:00)**

**What to show on screen:**
1. Open candidate detail view for `Priya Sharma`.
2. Point to the **Time in Stage** badge (e.g. `2 days 4 hours`).
3. Point to the **Audit Trail** timeline on the right side.
4. Click **"View Resume PDF"** to demonstrate opening the uploaded PDF file.

**What to say:**
> *"Here on the candidate profile page, we have two key features:
>
> 1. **Dynamic Stage Duration**: The time spent in the current stage is calculated dynamically on the server by computing the delta between `datetime.now()` and the timestamp of the candidate's last stage movement.
> 2. **Immutable Audit Ledger**: Every stage movement creates an append-only `StageHistory` record. Historical records are read-only and cannot be altered or deleted, providing complete compliance and accountability."*

---

### **Beat 5: Intelligent Natural Language Search & Fuzzy Matching (7:00 - 9:30)**

**What to show on screen:**
Perform the following 5 searches in the top search bar and show the result page for each:

1. Type `sharam`:
   - *Result*: Matches `Priya Sharma` using RapidFuzz string distance.
2. Type `Monday`:
   - *Result*: Parses `Moved since: Monday` and displays candidates moved since Monday.
3. Type `Screening > 7 days`:
   - *Result*: Shows candidates stuck in Screening for more than 7 days (`Aisha Khan`, `Kiran Patel`).
4. Type `Offer but not Hired`:
   - *Result*: Shows candidates who reached Offer but are not currently Hired (`Arjun Mehta`, `Vikram Singh`).
5. Type `xyz 123 gibberish`:
   - *Result*: Shows the **Query Understanding Box** explaining that the query wasn't recognized and providing query syntax examples.

**What to say:**
> *"Now let me demonstrate our Natural Language Search Engine built in `search/parser.py` and `search/ranking.py`:
>
> - **Fuzzy String Matching**: Searching for misspelling like `'sharam'` uses `RapidFuzz` Levenshtein scoring to correctly identify *Priya Sharma*.
> - **Date & Day Parsing**: Searching `'Monday'` automatically parses the day of the week and filters candidates moved since Monday.
> - **Relative Time Constraints**: Queries like `'Screening > 7 days'` filter candidates stuck in a stage for over a week.
> - **Boolean & Negative Filters**: Queries like `'Offer but not Hired'` identify candidates who reached the offer stage but did not join.
> - **Fallback Feedback**: When a search is unrecognized, the app displays a clear explanation box with supported query examples rather than failing silently."*

---

### **Beat 6: Automated Testing Verification Suite (9:30 - 10:30)**

**What to show on screen:**
1. Switch to terminal window.
2. Run command: `pytest`
3. Point out `12 passed in 0.11s`.

**What to say:**
> *"To ensure reliability, the application includes a comprehensive test suite written in `pytest`. Running `pytest` executes 12 unit and integration tests covering transition state rules, invalid move rejections, natural language query parsing, and fuzzy matching accuracy. All 12 tests pass."*

---

### **Beat 7: Architectural Design Decisions & AI Disagreement (10:30 - 12:00)**

**What to show on screen:**
- Briefly display `docs/ARCHITECTURE.md` or `docs/AI_CHAT_LOG.md`.

**What to say:**
> *"Finally, regarding architecture: the application follows a 3-tier modular design separating SQLAlchemy models, candidate and transition services, search parsing, and presentation routes.
>
> A key engineering decision I made during development was rejecting AI recommendations that suggested validating stage transitions only on the frontend via disabled form elements. I insisted on implementing backend validation in `services/transitions.py` so data integrity is guaranteed regardless of client-side interactions.
>
> Thank you! The application is fully functional, seeded, tested, and ready for deployment."*

---

## 📌 Summary Checklist for Recording

| Check | Item | Verified |
|:---:|---|:---:|
| ✅ | Virtual environment active (`.\venv\Scripts\activate`) | Yes |
| ✅ | Database seeded (`python seed.py`) | Yes |
| ✅ | Web server running (`python app.py`) | Yes |
| ✅ | Tested PDF Upload & mandatory field validation | Yes |
| ✅ | Tested Stage Transition (`Applied → Screening`) | Yes |
| ✅ | Tested Search queries (`sharam`, `Monday`, `Screening > 7 days`) | Yes |
| ✅ | Tested `pytest` command (12 passing tests) | Yes |
