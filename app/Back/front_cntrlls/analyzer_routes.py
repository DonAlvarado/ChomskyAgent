from flask import Blueprint, render_template

analyzer_bp = Blueprint("analyzer_bp", __name__)

@analyzer_bp.get("/analyzer")
def analyzer_page():
    return render_template("analyzer.html", title="Analizador")
