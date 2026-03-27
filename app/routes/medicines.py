from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import date, datetime
from app import db
from app.models.medicine import Medicine
from app.models.reminder import Reminder
from app.notifications.email_sender import send_email

medicines_bp = Blueprint("medicines", __name__, url_prefix="/medicines")


@medicines_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_medicine():
    if request.method == "POST":
        name          = request.form.get("name", "").strip()
        dosage        = request.form.get("dosage", "").strip()
        stock_count   = int(request.form.get("stock_count", 30))
        threshold     = int(request.form.get("low_stock_threshold", 5))
        reminder_time = request.form.get("reminder_time", "").strip()
        frequency     = request.form.get("frequency", "daily")

        if not name or not dosage:
            flash("Name and dosage are required.", "danger")
            return render_template("add_medicine.html")

        medicine = Medicine(
            user_id=current_user.id,
            name=name,
            dosage=dosage,
            stock_count=stock_count,
            low_stock_threshold=threshold,
        )
        db.session.add(medicine)
        db.session.flush()

        if reminder_time:
            reminder = Reminder(
                medicine_id=medicine.id,
                time=reminder_time,
                frequency=frequency,
                is_active=True,
            )
            db.session.add(reminder)

        db.session.commit()
        flash(f"'{name}' added successfully!", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("add_medicine.html")


@medicines_bp.route("/<int:medicine_id>/take", methods=["PUT", "POST"])
@login_required
def take_dose(medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id, user_id=current_user.id).first_or_404()

    if medicine.stock_count <= 0:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "out_of_stock", "stock": 0}), 400
        flash(f"'{medicine.name}' is out of stock!", "danger")
        return redirect(url_for("dashboard.dashboard"))

    medicine.stock_count -= 1

    # Mark reminders as taken today (clears missed flag)
    today = date.today()
    for reminder in medicine.reminders:
        reminder.last_taken   = today
        reminder.missed_today = False

    db.session.commit()

    # Dose taken confirmation email
    send_email(
        to=current_user.email,
        subject=f" Dose taken: {medicine.name}",
        body=(
            f"Hi {current_user.name},\n\n"
            f"This confirms that you just took a dose of:\n"
            f"  Medicine : {medicine.name}\n"
            f"  Dosage   : {medicine.dosage}\n"
            f"  Time     : {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n\n"
            f"Stock remaining : {medicine.stock_count} doses (~{medicine.days_remaining} days supply)\n"
            f"{' Running low — please refill soon!' if medicine.needs_refill else ' Stock level is good.'}\n\n"
            f"Stay healthy!\n"
            f"MediTrack"
        ),
    )

    # Separate low stock warning email
    if medicine.stock_count <= medicine.low_stock_threshold:
        send_email(
            to=current_user.email,
            subject=f" Low stock alert: {medicine.name}",
            body=(
                f"Hi {current_user.name},\n\n"
                f"'{medicine.name}' is running low.\n"
                f"Remaining: {medicine.stock_count} doses (~{medicine.days_remaining} days).\n\n"
                f"Please refill soon.\n"
                f"MediTrack"
            ),
        )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "stock":          medicine.stock_count,
            "status":         medicine.stock_status,
            "days_remaining": medicine.days_remaining,
        })

    flash(f"Dose taken! {medicine.stock_count} doses (~{medicine.days_remaining} days) remaining.", "success")
    return redirect(url_for("dashboard.dashboard"))


@medicines_bp.route("/<int:medicine_id>/stock", methods=["PUT", "POST"])
@login_required
def refill_stock(medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id, user_id=current_user.id).first_or_404()
    amount = int(request.form.get("amount", 0))

    if amount <= 0:
        flash("Refill amount must be greater than 0.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    medicine.stock_count += amount
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "stock":          medicine.stock_count,
            "status":         medicine.stock_status,
            "days_remaining": medicine.days_remaining,
        })

    flash(f"Refilled '{medicine.name}' by {amount}. New stock: {medicine.stock_count}.", "success")
    return redirect(url_for("dashboard.dashboard"))


@medicines_bp.route("/<int:medicine_id>/delete", methods=["POST"])
@login_required
def delete_medicine(medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id, user_id=current_user.id).first_or_404()
    name = medicine.name
    db.session.delete(medicine)
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"deleted": True})

    flash(f"'{name}' deleted.", "info")
    return redirect(url_for("dashboard.dashboard"))


@medicines_bp.route("/api/stock-alerts")
@login_required
def stock_alerts():
    low = Medicine.query.filter(
        Medicine.user_id == current_user.id,
        Medicine.stock_count <= Medicine.low_stock_threshold,
    ).all()
    return jsonify([
        {
            "id":             m.id,
            "name":           m.name,
            "stock":          m.stock_count,
            "status":         m.stock_status,
            "days_remaining": m.days_remaining,
        }
        for m in low
    ])