from flask import Blueprint, render_template

chat_bp = Blueprint("chat_bp", __name__)

@chat_bp.get("/chat")
def chat_page():
    return render_template("chat.html", title="Chat IA")
