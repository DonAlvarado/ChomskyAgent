from flask import Blueprint, request, jsonify
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.equivalence_checker import equivalent
from Back.utils.validators import is_valid_grammar

compare_api_bp = Blueprint("compare_api_bp", __name__)

@compare_api_bp.post("/grammars")
def compare_grammars_api():
    data = request.get_json() or {}
    g1 = data.get("g1", [])
    g2 = data.get("g2", [])

    if not is_valid_grammar(g1) or not is_valid_grammar(g2):
        return jsonify({"success": False, "error": "Gramáticas inválidas."}), 400

    try:
        g1_obj = classify_grammar(parse_grammar(g1))
        g2_obj = classify_grammar(parse_grammar(g2))

        result = equivalent(g1_obj, g2_obj)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
