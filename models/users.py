import datetime
import uuid

from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.timezone.utc)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.timezone.utc, onupdate=datetime.datetime.utcnow)
