from flask import Blueprint, render_template

tutor_bp = Blueprint("tutor_bp", __name__)

@tutor_bp.get("/tutor")
def tutor_page():
    return render_template("tutor.html", title="Modo Tutor")
