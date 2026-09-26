from datetime import datetime, timezone
from models import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    resume_url = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    current_stage = db.Column(db.String(50), nullable=False, default='Applied')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    history = db.relationship('StageHistory', backref='candidate', lazy=True, cascade="all, delete-orphan", order_by="StageHistory.timestamp")

    def __repr__(self):
        return f'<Candidate {self.name} - {self.current_stage}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'resume_url': self.resume_url,
            'notes': self.notes,
            'current_stage': self.current_stage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
