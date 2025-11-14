from flask import Blueprint, request, jsonify

from Back.classifier.explainable_ai import ExplainableAI
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.automata_parser import parse_automaton
from Back.classifier.converter import regex_to_nfa_epsilon, nfa_epsilon_to_dfa

from Back.utils.validators import (
    is_valid_regex,
    is_valid_grammar,
    is_valid_automaton
)
from Back.utils.logger import get_logger

agent_api_bp = Blueprint("agent_api_bp", __name__)
ai = ExplainableAI()
log = get_logger("AgentAPI")


@agent_api_bp.post("/message")
def agent_message():
    data = request.get_json() or {}
    msg = data.get("message", "").lower()
    log.info(f"Mensaje recibido del usuario: {msg}")

    try:
        if "analiza esta gramática" in msg or "clasifica" in msg:
            rules = data.get("rules", [])
            if not is_valid_grammar(rules):
                return jsonify({"reply": "La gramática no es válida."})

            g = classify_grammar(parse_grammar(rules))
            explanation = ai.explain_grammar_classification(g)
            return jsonify({"reply": explanation})

        if "explica este automata" in msg or "qué tipo es" in msg:
            automaton = data.get("automaton", {})
            if not is_valid_automaton(automaton):
                return jsonify({"reply": "El autómata no es válido."})

            a = parse_automaton(automaton)
            explanation = ai.explain_automaton(a)
            return jsonify({"reply": explanation})

        if "regex" in msg:
            regex = data.get("regex", "")
            if not is_valid_regex(regex):
                return jsonify({"reply": "La expresión regular no es válida."})

            nfa = regex_to_nfa_epsilon(regex)
            dfa = nfa_epsilon_to_dfa(nfa)
            explanation = ai.explain_regex_conversion(regex, nfa, dfa)
            return jsonify({"reply": explanation})

        return jsonify({"reply": "No entendí tu solicitud, dame más contexto."})

    except Exception as e:
        log.error(f"Error en AgentAPI: {str(e)}")
        return jsonify({"reply": f"Error interno: {str(e)}"})
