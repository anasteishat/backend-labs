from datetime import datetime
from app import db
from datetime import timezone

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='account')
    records = db.relationship('Record', back_populates='account', cascade='all, delete-orphan')

    def increase_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def decrease_balance(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount 