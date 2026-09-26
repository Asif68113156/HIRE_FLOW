from datetime import datetime, timezone
from models import db, Candidate, StageHistory
from services.transitions import validate_stage_transition

def create_candidate(name, email, phone, role, resume_url=None, notes=None):
    if not name or not str(name).strip():
        raise ValueError("Full Name is mandatory.")
    if not email or not str(email).strip():
        raise ValueError("Email address is mandatory.")
    if not phone or not str(phone).strip():
        raise ValueError("Phone number is mandatory.")
    if not role or not str(role).strip():
        raise ValueError("Job Role is mandatory.")
    if not resume_url or not str(resume_url).strip():
        raise ValueError("Resume PDF file is mandatory.")
    if not notes or not str(notes).strip():
        raise ValueError("Notes field is mandatory.")

    if Candidate.query.filter_by(email=email.strip()).first() is not None:
        raise ValueError(f"Candidate with email {email.strip()} already exists.")
        
    candidate = Candidate(
        name=name.strip(),
        email=email.strip(),
        phone=phone.strip(),
        role=role.strip(),
        resume_url=resume_url.strip(),
        notes=notes.strip(),
        current_stage='Applied'
    )
    
    db.session.add(candidate)
    db.session.flush()
    
    history = StageHistory(
        candidate_id=candidate.id,
        from_stage=None,
        to_stage='Applied',
        actor='Recruiter'
    )
    
    db.session.add(history)
    db.session.commit()
    
    return candidate

def advance_candidate_stage(candidate_id, next_stage, actor='Recruiter'):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        raise ValueError("Candidate not found.")
        
    current_stage = candidate.current_stage
    
    validate_stage_transition(current_stage, next_stage)
    
    candidate.current_stage = next_stage
    candidate.updated_at = datetime.now(timezone.utc)
    
    history = StageHistory(
        candidate_id=candidate.id,
        from_stage=current_stage,
        to_stage=next_stage,
        actor=actor
    )
    
    db.session.add(history)
    db.session.commit()
    
    return candidate

def get_candidate_stage_duration(candidate_id):
    history = StageHistory.query.filter_by(candidate_id=candidate_id).order_by(StageHistory.timestamp.desc()).first()
    
    if not history:
        return "Unknown"
        
    now = datetime.now(timezone.utc)
    ts = history.timestamp
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
        
    duration = now - ts
    
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days} days {hours} hours"
    elif hours > 0:
        return f"{hours} hours {minutes} minutes"
    elif minutes > 0:
        return f"{minutes} minutes"
    else:
        return "Just now"
