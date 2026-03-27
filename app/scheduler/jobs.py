from datetime import datetime, date, timedelta


def remind_job(app):
    """Runs every minute. Sends reminder emails and flags missed doses."""
    with app.app_context():
        from app.models.reminder import Reminder
        from app.notifications.email_sender import send_email
        from app import db

        now       = datetime.now()
        now_hhmm  = now.strftime("%H:%M")
        today     = date.today()

        for reminder in Reminder.query.filter_by(is_active=True).all():
            medicine = reminder.medicine
            user     = medicine.owner

            # ── Send reminder email ──────────────────────────
            if reminder.time == now_hhmm and reminder.last_sent != today:
                sent = send_email(
                    to=user.email,
                    subject=f"Reminder: time to take {medicine.name}",
                    body=(
                        f"Hi {user.name},\n\n"
                        f"Time to take {medicine.name} ({medicine.dosage}).\n"
                        f"Stock remaining: {medicine.stock_count} doses "
                        f"(~{medicine.days_remaining} days).\n\n"
                        f"Stay healthy!\nMediBuddy"
                    ),
                )
                if sent:
                    reminder.last_sent    = today
                    reminder.missed_today = True   # assume missed until Take dose pressed
                    db.session.commit()

            # ── Flag missed dose (30 min grace window) ───────
            hh, mm = map(int, reminder.time.split(":"))
            fire_time    = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
            grace_cutoff = fire_time + timedelta(minutes=30)

            if (
                now > grace_cutoff
                and reminder.missed_today
                and reminder.last_taken != today
                and reminder.last_sent == today
            ):
                # Already past grace — stays flagged as missed
                pass


def stock_alert_job(app):
    """Runs every hour. Sends stock-low and refill-needed alerts."""
    with app.app_context():
        from app.models.medicine import Medicine
        from app.notifications.email_sender import send_email

        for medicine in Medicine.query.filter(
            Medicine.stock_count <= Medicine.low_stock_threshold
        ).all():
            user = medicine.owner
            send_email(
                to=user.email,
                subject=f"Stock alert: {medicine.name} is running low",
                body=(
                    f"Hi {user.name},\n\n"
                    f"'{medicine.name}' has only {medicine.stock_count} doses left "
                    f"(~{medicine.days_remaining} days supply).\n"
                    f"Threshold: {medicine.low_stock_threshold} doses.\n\n"
                    f"Please refill soon.\nMediBuddy"
                ),
            )