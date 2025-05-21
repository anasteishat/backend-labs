from datetime import datetime
from app import db
from datetime import timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    records = db.relationship('Record', back_populates='user', cascade='all, delete-orphan')
    account = db.relationship('Account', back_populates='user', uselist=False, cascade='all, delete-orphan')