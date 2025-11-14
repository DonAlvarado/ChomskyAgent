from flask import Blueprint, request, jsonify
from Back.classifier.converter import DFA
from Back.classifier.visualizer import DFAVisualizer

from Back.utils.validators import is_valid_automaton
from Back.utils.logger import get_logger

viz_api_bp = Blueprint("viz_api_bp", __name__)
log = get_logger("VisualizerAPI")


@viz_api_bp.post("/dfa")
def viz_dfa():
    data = request.get_json() or {}

    if not is_valid_automaton(data):
        return jsonify({"success": False, "error": "Autómata inválido."}), 400

    try:
        dfa = DFA(
            states=set(data["states"]),
            alphabet=set(data["alphabet"]),
            start=data["start"],
            accept=set(data["accept"]),
            transitions=data["transitions"]
        )

        svg = DFAVisualizer().visualize(dfa)

        return jsonify({"success": True, "svg": svg})

    except Exception as e:
        log.error(f"Error visualizando DFA: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
