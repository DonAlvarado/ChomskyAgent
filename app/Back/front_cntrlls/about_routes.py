from flask import Blueprint, render_template

about_bp = Blueprint("about_bp", __name__)

@about_bp.get("/about")
def about_page():
    return render_template("about.html", title="Acerca de")
