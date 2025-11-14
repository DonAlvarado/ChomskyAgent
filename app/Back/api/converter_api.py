from flask import Blueprint, request, jsonify

from Back.classifier.converter import (
    regex_to_nfa_epsilon,
    nfa_epsilon_to_dfa,
    dfa_to_regular_grammar
)

from Back.classifier.dfa_minimizer import minimize_dfa

from Back.utils.validators import is_valid_regex
from Back.utils.logger import get_logger

converter_api_bp = Blueprint("converter_api_bp", __name__)
log = get_logger("ConverterAPI")


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

    if not is_valid_regex(regex):
        log.error(f"Regex inválida: {regex}")
        return jsonify({"success": False, "error": "Expresión regular inválida."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        return jsonify({"success": True, "regex": regex, "nfa": _nfa_to_dict(nfa)})
    except Exception as e:
        log.error(f"Error en regex2nfa: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


@converter_api_bp.post("/regex2afd")
def regex_to_afd():
    data = request.get_json() or {}
    regex = data.get("regex", "")

    if not is_valid_regex(regex):
        return jsonify({"success": False, "error": "Expresión regular inválida."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)
        return jsonify({"success": True, "regex": regex, "afd": _dfa_to_dict(dfa)})
    except Exception as e:
        log.error(f"Error en regex2afd: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


@converter_api_bp.post("/regex2grammar")
def regex_to_grammar():
    data = request.get_json() or {}
    regex = data.get("regex", "")

    if not is_valid_regex(regex):
        return jsonify({"success": False, "error": "Expresión regular inválida."}), 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)
        grammar = dfa_to_regular_grammar(dfa)

        return jsonify({"success": True, "regex": regex, "grammar": grammar})
    except Exception as e:
        log.error(f"Error en regex2grammar: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


@converter_api_bp.post("/regex2afd_min")
def regex_to_afd_min():
    data = request.get_json(force=True)
    regex = data.get("regex", "").strip()

    if not is_valid_regex(regex):
        return {"success": False, "error": "Expresión regular inválida."}, 400

    try:
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)

        min_dfa = minimize_dfa(dfa)

        return {
            "success": True,
            "regex": regex,
            "afd_min": _dfa_to_dict(min_dfa)
        }
    except Exception as e:
        log.error(f"Error en minimización DFA: {str(e)}")
        return {"success": False, "error": str(e)}, 500
