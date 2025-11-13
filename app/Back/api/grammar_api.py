from flask import Blueprint, request, jsonify

from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar


grammar_api_bp = Blueprint("grammar_api_bp", __name__)


@grammar_api_bp.post("/analyze")
def analyze_grammar():
    data = request.get_json() or {}
    rules = data.get("rules") or []
    start_symbol = data.get("start_symbol")

    try:
        g = parse_grammar(rules, start_symbol)
        g = classify_grammar(g)

        return jsonify({
            "success": True,
            "grammar": g.to_dict(),
            "classification": g.metadata.get("classification", {})
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error interno: {str(e)}"
        }), 500
