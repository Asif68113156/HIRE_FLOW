import os
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from app import create_app
from models import db, Candidate, StageHistory

app = create_app()

def clear_db():
    db.session.query(StageHistory).delete()
    db.session.query(Candidate).delete()
    db.session.commit()

def add_history(candidate_id, from_stage, to_stage, timestamp, actor='Recruiter'):
    h = StageHistory(
        candidate_id=candidate_id,
        from_stage=from_stage,
        to_stage=to_stage,
        timestamp=timestamp,
        actor=actor
    )
    db.session.add(h)

def create_seed_data():
    now = datetime.now(timezone.utc)
    
    last_monday = now + relativedelta(weekday=MO(-1), hour=14)
    if (now - last_monday).days == 0:
        last_monday = now + relativedelta(weekday=MO(-2), hour=14)
        
    last_week_older = now - timedelta(days=9)
    yesterday = now - timedelta(days=1)
    two_hours_ago = now - timedelta(hours=2)
    sample_pdf = "/static/uploads/resumes/sample_resume.pdf"

    with app.app_context():
        clear_db()
        
        c1 = Candidate(name="Priya Sharma", email="priya@example.com", phone="555-0101", role="Software Engineer", resume_url=sample_pdf, notes="Strong algorithmic problem solving skills.", current_stage="Interview", created_at=last_monday - timedelta(days=5))
        db.session.add(c1)
        db.session.flush()
        add_history(c1.id, None, "Applied", c1.created_at)
        add_history(c1.id, "Applied", "Screening", last_week_older)
        add_history(c1.id, "Screening", "Interview", last_monday)

        c2 = Candidate(name="Rahul Patil", email="rahul@example.com", phone="555-0102", role="Product Manager", resume_url=sample_pdf, notes="Lacks technical background for engineering team requirements.", current_stage="Rejected", created_at=last_week_older)
        db.session.add(c2)
        db.session.flush()
        add_history(c2.id, None, "Applied", c2.created_at)
        add_history(c2.id, "Applied", "Screening", last_week_older + timedelta(days=2))
        add_history(c2.id, "Screening", "Rejected", yesterday)

        c3 = Candidate(name="Aisha Khan", email="aisha@example.com", phone="555-0103", role="UX Designer", resume_url=sample_pdf, notes="Portfolio review pending senior designer availability.", current_stage="Screening", created_at=last_week_older - timedelta(days=2))
        db.session.add(c3)
        db.session.flush()
        add_history(c3.id, None, "Applied", c3.created_at)
        add_history(c3.id, "Applied", "Screening", last_week_older)

        c4 = Candidate(name="Arjun Mehta", email="arjun@example.com", phone="555-0104", role="Data Scientist", resume_url=sample_pdf, notes="Offer letter generated, waiting for candidate response.", current_stage="Offer", created_at=now - timedelta(days=15))
        db.session.add(c4)
        db.session.flush()
        add_history(c4.id, None, "Applied", c4.created_at)
        add_history(c4.id, "Applied", "Screening", now - timedelta(days=10))
        add_history(c4.id, "Screening", "Interview", now - timedelta(days=5))
        add_history(c4.id, "Interview", "Offer", yesterday)

        c5 = Candidate(name="Neha Joshi", email="neha@example.com", phone="555-0105", role="DevOps Engineer", resume_url=sample_pdf, notes="Accepted offer. Onboarding starts next month.", current_stage="Hired", created_at=now - timedelta(days=20))
        db.session.add(c5)
        db.session.flush()
        add_history(c5.id, None, "Applied", c5.created_at)
        add_history(c5.id, "Applied", "Screening", now - timedelta(days=18))
        add_history(c5.id, "Screening", "Interview", now - timedelta(days=14))
        add_history(c5.id, "Interview", "Offer", now - timedelta(days=7))
        add_history(c5.id, "Offer", "Hired", two_hours_ago)

        c6 = Candidate(name="Rohan Desai", email="rohan@example.com", phone="555-0106", role="Frontend Developer", resume_url=sample_pdf, notes="Initial application received.", current_stage="Applied", created_at=two_hours_ago)
        db.session.add(c6)
        db.session.flush()
        add_history(c6.id, None, "Applied", c6.created_at)

        c7 = Candidate(name="Sneha Kulkarni", email="sneha@example.com", phone="555-0107", role="Backend Developer", resume_url=sample_pdf, notes="Screening call scheduled for tomorrow.", current_stage="Screening", created_at=now - timedelta(days=3))
        db.session.add(c7)
        db.session.flush()
        add_history(c7.id, None, "Applied", c7.created_at)
        add_history(c7.id, "Applied", "Screening", two_hours_ago)

        c8 = Candidate(name="Aman Verma", email="aman@example.com", phone="555-0108", role="QA Engineer", resume_url=sample_pdf, notes="System architecture interview completed successfully.", current_stage="Interview", created_at=now - timedelta(days=12))
        db.session.add(c8)
        db.session.flush()
        add_history(c8.id, None, "Applied", c8.created_at)
        add_history(c8.id, "Applied", "Screening", now - timedelta(days=10))
        add_history(c8.id, "Screening", "Interview", yesterday)

        c10 = Candidate(name="Kiran Patel", email="kiran@example.com", phone="555-0110", role="DBA", resume_url=sample_pdf, notes="Awaiting background verification checks.", current_stage="Screening", created_at=now - timedelta(days=25))
        db.session.add(c10)
        db.session.flush()
        add_history(c10.id, None, "Applied", c10.created_at)
        add_history(c10.id, "Applied", "Screening", now - timedelta(days=22))

        c11 = Candidate(name="Vikram Singh", email="vikram@example.com", phone="555-0111", role="Security Analyst", resume_url=sample_pdf, notes="Declined offer due to location constraints.", current_stage="Rejected", created_at=now - timedelta(days=10))
        db.session.add(c11)
        db.session.flush()
        add_history(c11.id, None, "Applied", c11.created_at)
        add_history(c11.id, "Applied", "Screening", now - timedelta(days=8))
        add_history(c11.id, "Screening", "Interview", now - timedelta(days=6))
        add_history(c11.id, "Interview", "Offer", now - timedelta(days=4))
        add_history(c11.id, "Offer", "Rejected", yesterday) 

        c12 = Candidate(name="Pooja Reddy", email="pooja@example.com", phone="555-0112", role="HR Manager", resume_url=sample_pdf, notes="Second round leadership interview scheduled.", current_stage="Interview", created_at=now - timedelta(days=5))
        db.session.add(c12)
        db.session.flush()
        add_history(c12.id, None, "Applied", c12.created_at)
        add_history(c12.id, "Applied", "Screening", now - timedelta(days=3))
        add_history(c12.id, "Screening", "Interview", two_hours_ago)

        db.session.commit()
        print("Database seeded with candidates!")

if __name__ == '__main__':
    create_seed_data()
