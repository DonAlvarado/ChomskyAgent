from flask import Blueprint, render_template

converter_routes_bp = Blueprint("converter_routes_bp", __name__)


@converter_routes_bp.get("/converter")
def converter_page():
    return render_template("converter.html")
