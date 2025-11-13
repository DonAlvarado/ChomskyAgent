# app/Back/front_cntrlls/home_routes.py

from flask import Blueprint, render_template

home_bp = Blueprint("home_bp", __name__)

@home_bp.get("/")
def intro_page():
    return render_template("intro.html", title="Inicio")
