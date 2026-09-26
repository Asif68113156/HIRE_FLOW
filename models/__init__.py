from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.candidate import Candidate
from models.history import StageHistory

__all__ = ['db', 'Candidate', 'StageHistory']
