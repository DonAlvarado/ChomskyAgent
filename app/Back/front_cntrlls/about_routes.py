from flask import Blueprint, render_template

about_bp = Blueprint("about_bp", __name__, url_prefix="/about")

@about_bp.get("/")
def about_page():
    return render_template("about.html")
