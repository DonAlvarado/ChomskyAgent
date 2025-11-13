from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.get("/dashboard")
def dashboard_page():
    return render_template("dashboard.html", title="Dashboard")
