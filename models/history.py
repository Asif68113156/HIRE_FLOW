from datetime import datetime, timezone
from models import db

class StageHistory(db.Model):
    __tablename__ = 'stage_history'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    from_stage = db.Column(db.String(50), nullable=True)
    to_stage = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    actor = db.Column(db.String(100), nullable=False, default='Recruiter')
    
    def __repr__(self):
        return f'<StageHistory {self.candidate_id}: {self.from_stage} -> {self.to_stage}>'

    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'from_stage': self.from_stage,
            'to_stage': self.to_stage,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'actor': self.actor
        }
