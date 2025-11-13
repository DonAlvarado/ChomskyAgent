from flask import Blueprint, request, jsonify

from Back.classifier.explainable_ai import ExplainableAI
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.automata_parser import parse_automaton
from Back.classifier.converter import regex_to_nfa_epsilon, nfa_epsilon_to_dfa

agent_api_bp = Blueprint("agent_api_bp", __name__)
ai = ExplainableAI()


@agent_api_bp.post("/message")
def agent_message():
    data = request.get_json() or {}
    msg = data.get("message", "").lower()

    try:
        if "analiza esta gramática" in msg or "clasifica" in msg:
            rules = data.get("rules", [])
            g = parse_grammar(rules)
            g = classify_grammar(g)
            explanation = ai.explain_grammar_classification(g)
            return jsonify({"reply": explanation})

        if "explica este automata" in msg or "qué tipo es" in msg:
            a = parse_automaton(data.get("automaton", {}))
            explanation = ai.explain_automaton(a)
            return jsonify({"reply": explanation})

        if "regex" in msg:
            regex = data.get("regex", "")
            nfa = regex_to_nfa_epsilon(regex)
            dfa = nfa_epsilon_to_dfa(nfa)
            explanation = ai.explain_regex_conversion(regex, nfa, dfa)
            return jsonify({"reply": explanation})

        return jsonify({"reply": "No entendí tu solicitud, dame más contexto."})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})
