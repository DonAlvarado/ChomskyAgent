from flask import Blueprint, request, jsonify

from Back.classifier.converter import (
    regex_to_nfa_epsilon,
    nfa_epsilon_to_dfa,
    dfa_to_regular_grammar,
    grammar_to_afd,
)

converter_api_bp = Blueprint("converter_api_bp", __name__)


def _nfa_to_dict(nfa):
    return {
        "states": sorted(list(nfa.states)),
        "alphabet": sorted(list(nfa.alphabet)),
        "start": nfa.start,
        "accept": sorted(list(nfa.accept)),
        "transitions": nfa.transitions,
    }


def _dfa_to_dict(dfa):
    return {
        "states": sorted(list(dfa.states)),
        "alphabet": sorted(list(dfa.alphabet)),
        "start": dfa.start,
        "accept": sorted(list(dfa.accept)),
        "transitions": dfa.transitions,
    }


@converter_api_bp.post("/regex2nfa")
def regex_to_nfa():
    data = request.get_json() or {}
    regex = data.get("regex", "")

    if not regex:
        return jsonify({"success": False, "error": "No se recibió expresión regular."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        return jsonify({
            "success": True,
            "regex": regex,
            "nfa": _nfa_to_dict(nfa),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@converter_api_bp.post("/regex2afd")
def regex_to_afd():
    data = request.get_json() or {}
    regex = data.get("regex", "")

    if not regex:
        return jsonify({"success": False, "error": "No se recibió expresión regular."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)
        return jsonify({
            "success": True,
            "regex": regex,
            "afd": _dfa_to_dict(dfa),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@converter_api_bp.post("/regex2grammar")
def regex_to_grammar():
    data = request.get_json() or {}
    regex = data.get("regex", "")

    if not regex:
        return jsonify({"success": False, "error": "No se recibió expresión regular."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)
        grammar = dfa_to_regular_grammar(dfa)

        return jsonify({
            "success": True,
            "regex": regex,
            "grammar": grammar,
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@converter_api_bp.post("/regex2afd_min")
def regex_to_afd_min():
    data = request.get_json(force=True)
    regex = data.get("regex", "").strip()
    if not regex:
        return {"error": "Falta regex"}, 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)

        # Minimización
        from Back.classifier.dfa_minimizer import minimize_dfa
        min_dfa = minimize_dfa(dfa)

        return {
            "success": True,
            "regex": regex,
            "afd_min": {
                "states": list(min_dfa.states),
                "alphabet": list(min_dfa.alphabet),
                "start": min_dfa.start,
                "accept": list(min_dfa.accept),
                "transitions": min_dfa.transitions
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}, 500
