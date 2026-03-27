from app import db
from datetime import datetime


class Reminder(db.Model):
    __tablename__ = "reminders"

    id           = db.Column(db.Integer, primary_key=True)
    medicine_id  = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)
    time         = db.Column(db.String(5), nullable=False)   # "HH:MM"
    frequency    = db.Column(db.String(10), default="daily") # "daily" | "weekly"
    is_active    = db.Column(db.Boolean, default=True)
    last_sent    = db.Column(db.Date, nullable=True)
    last_taken   = db.Column(db.Date, nullable=True)         # set when user presses Take dose
    missed_today = db.Column(db.Boolean, default=False)      # flagged by scheduler

    @property
    def next_dose_seconds(self):
        """Seconds until this reminder fires next (today or tomorrow)."""
        from datetime import date, timedelta
        now = datetime.now()
        hh, mm = map(int, self.time.split(":"))
        today_fire = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if today_fire > now:
            delta = today_fire - now
        else:
            tomorrow_fire = today_fire + timedelta(days=1)
            delta = tomorrow_fire - now
        return int(delta.total_seconds())

    def __repr__(self):
        return f"<Reminder {self.time} for medicine_id={self.medicine_id}>"