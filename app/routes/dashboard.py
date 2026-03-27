from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.medicine import Medicine

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    medicines = (
        Medicine.query
        .filter_by(user_id=current_user.id)
        .order_by(Medicine.name)
        .all()
    )

    stats = {
        "total": len(medicines),
        "low":   sum(1 for m in medicines if m.stock_status == "low"),
        "empty": sum(1 for m in medicines if m.stock_status == "empty"),
    }

    return render_template("dashboard.html", medicines=medicines, stats=stats)