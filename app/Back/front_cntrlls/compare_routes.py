from flask import Blueprint, render_template

compare_routes_bp = Blueprint("compare_routes_bp", __name__)

@compare_routes_bp.get("/compare")
def compare_view():
    return render_template("compare.html")
