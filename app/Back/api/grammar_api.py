from flask import Blueprint, request, jsonify

from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar

from Back.utils.validators import is_valid_grammar
from Back.utils.logger import get_logger

grammar_api_bp = Blueprint("grammar_api_bp", __name__)
log = get_logger("GrammarAPI")


@grammar_api_bp.post("/analyze")
def analyze_grammar():
    data = request.get_json() or {}
    rules = data.get("rules") or []
    start_symbol = data.get("start_symbol")

    if not is_valid_grammar(rules):
        return jsonify({"success": False, "error": "Gramática inválida."}), 400

    try:
        g = classify_grammar(parse_grammar(rules, start_symbol))
        return jsonify({
            "success": True,
            "grammar": g.to_dict(),
            "classification": g.metadata.get("classification", {})
        })

    except Exception as e:
        log.error(f"Error analizando gramática: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error interno: {str(e)}"
        }), 500
