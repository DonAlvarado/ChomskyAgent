from flask import Blueprint, request, jsonify

from Back.classifier.explainable_ai import ExplainableAI
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.automata_parser import parse_automaton
from Back.classifier.converter import regex_to_nfa_epsilon, nfa_epsilon_to_dfa

from AI.chatbot import Chatbot

from Back.utils.validators import (
    is_valid_regex,
    is_valid_grammar,
    is_valid_automaton
)
from Back.utils.logger import get_logger


agent_api_bp = Blueprint("agent_api_bp", __name__)
ai = ExplainableAI()
log = get_logger("AgentAPI")

# Instancia del Chatbot
chatbot = Chatbot(base_url="http://localhost:5000")


# ENDPOINT LEGACY
@agent_api_bp.post("/message")
def agent_message():
    data = request.get_json() or {}
    msg = data.get("message", "").lower()
    log.info(f"Mensaje recibido del usuario: {msg}")

    try:
        # Gramática
        if "analiza esta gramática" in msg or "clasifica" in msg:
            rules = data.get("rules", [])
            if not is_valid_grammar(rules):
                return jsonify({"reply": "La gramática no es válida."})

            g = classify_grammar(parse_grammar(rules))
            explanation = ai.explain_grammar(g)
            return jsonify({"reply": explanation})

        # Autómata
        if "explica este automata" in msg or "qué tipo es" in msg:
            automaton = data.get("automaton", {})
            if not is_valid_automaton(automaton):
                return jsonify({"reply": "El autómata no es válido."})

            a = parse_automaton(automaton)
            explanation = ai.explain_grammar(a)
            return jsonify({"reply": explanation})

        # Regex
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


# ENDPOINT DEL CHAT
@agent_api_bp.post("/chat")
def chat_endpoint():
    try:
        data = request.get_json() or {}
        msg = data.get("message", "").strip()

        if not msg:
            return jsonify({"reply": "Dime algo relacionado con gramáticas, autómatas o regex y te ayudo."})

        result = chatbot.handle_message(msg)

        return jsonify({
            "reply": result["reply"],
            "intent": result["intent"]
        })

    except Exception as e:
        log.error(f"Error en AgentAPI: {str(e)}")
        return jsonify({"reply": f"Error interno: {str(e)}"})
