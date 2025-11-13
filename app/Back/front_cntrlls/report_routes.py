from flask import Blueprint, render_template

report_pages_bp = Blueprint("report_pages_bp", __name__)

@report_pages_bp.get("/reports")
def reports_page():
    return render_template("reports.html", title="Reportes")
