from flask import Blueprint, request, jsonify
from Back.classifier.tutor_quiz import TutorQuiz

from Back.utils.logger import get_logger

tutor_api_bp = Blueprint("tutor_api_bp", __name__)
quiz = TutorQuiz()
log = get_logger("TutorAPI")


@tutor_api_bp.post("/question")
def generate_question():
    data = request.get_json() or {}
    difficulty = data.get("difficulty", "basic")

    q = quiz.make_question(difficulty)

    if "error" in q:
        log.error(f"Error generando pregunta: {q['error']}")
        return jsonify({"success": False, "error": q["error"]}), 400

    return jsonify({
        "success": True,
        "id": q["id"],
        "type": q["type"],
        "question": q["question"]
    })


@tutor_api_bp.post("/check")
def check_answer():
    data = request.get_json() or {}
    qtype = data.get("type")
    question = data.get("question") or {}
    answer = data.get("answer", "")

    try:
        result = quiz.check_answer(qtype, question, answer)

        return jsonify({
            "success": True,
            "correct": result["correct"],
            "correct_type": result["correct_type"]
        })

    except Exception as e:
        log.error(f"Error evaluando respuesta: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
