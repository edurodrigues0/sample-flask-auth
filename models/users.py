from app import db
import datetime
import uuid

class User(db.Model):
  id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
  name = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(), nullable=False)
  created_at = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.Datetime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
