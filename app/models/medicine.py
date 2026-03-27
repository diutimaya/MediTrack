from app import db
from datetime import datetime


class Medicine(db.Model):
    __tablename__ = "medicines"

    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name                = db.Column(db.String(150), nullable=False)
    dosage              = db.Column(db.String(100), nullable=False)
    stock_count         = db.Column(db.Integer, default=30, nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=5, nullable=False)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)

    reminders = db.relationship("Reminder", backref="medicine", lazy=True, cascade="all, delete-orphan")

    @property
    def doses_per_day(self):
        """Count active daily reminders as doses per day."""
        return max(1, sum(1 for r in self.reminders if r.is_active and r.frequency == "daily"))

    @property
    def days_remaining(self):
        """How many days of stock left based on doses per day."""
        if self.stock_count <= 0:
            return 0
        return self.stock_count // self.doses_per_day

    @property
    def needs_refill(self):
        """True if less than 7 days of stock remaining."""
        return self.days_remaining < 7

    @property
    def stock_status(self):
        if self.stock_count == 0:
            return "empty"
        if self.stock_count <= self.low_stock_threshold:
            return "low"
        return "ok"

    def __repr__(self):
        return f"<Medicine {self.name}>"