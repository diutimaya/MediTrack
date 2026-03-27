from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.medicine import Medicine

stock_bp = Blueprint("stock", __name__, url_prefix="/stock")


@stock_bp.route("/")
@login_required
def stock_summary():
    medicines = (
        Medicine.query
        .filter_by(user_id=current_user.id)
        .order_by(Medicine.name)
        .all()
    )

    critical = [m for m in medicines if m.stock_count == 0]
    low      = [m for m in medicines if 0 < m.stock_count <= m.low_stock_threshold]
    refill   = [m for m in medicines if m.needs_refill and m.stock_count > m.low_stock_threshold]
    ok       = [m for m in medicines if not m.needs_refill and m.stock_count > 0]

    return render_template(
        "stock_summary.html",
        critical=critical,
        low=low,
        refill=refill,
        ok=ok,
        total=len(medicines),
    )