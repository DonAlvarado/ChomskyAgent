from __future__ import annotations
from typing import Dict, Any

from Back.interfaces.IAnalyzer import IAnalyzer
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar

from Back.classifier.automata_parser import (
    parse_automaton,
    detect_type
)

from Back.classifier.converter import (
    regex_to_nfa_epsilon,
    nfa_epsilon_to_dfa
)

from Back.utils.validators import (
    is_valid_regex,
    is_valid_automaton,
)
from Back.utils.logger import get_logger

log = get_logger("Analyzers")


class GrammarAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        rules = data.get("rules") or []
        start = data.get("start_symbol")

        # Aquí dejamos que grammar_parser sea el que valide en detalle.
        try:
            g = parse_grammar(rules, start)
            g = classify_grammar(g)

            log.info("Gramática analizada y clasificada correctamente.")
            return {
                "success": True,
                "grammar": g.to_dict(),
                "classification": g.metadata.get("classification")
            }
        except Exception as e:
            log.error(f"Error analizando gramática: {e}")
            return {"success": False, "error": str(e)}


class AutomataAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not is_valid_automaton(data):
            log.error("Autómata inválido recibido en AutomataAnalyzer.")
            return {"success": False, "error": "Autómata inválido."}

        try:
            a = parse_automaton(data)
            t = detect_type(a)
            log.info(f"Autómata analizado. Tipo detectado: {t}")

            return {
                "success": True,
                "automaton": a.to_dict(),
                "type": t
            }
        except Exception as e:
            log.error(f"Error analizando autómata: {e}")
            return {"success": False, "error": str(e)}


class RegexAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        regex = data.get("regex", "")

        if not is_valid_regex(regex):
            log.error(f"Regex inválida en RegexAnalyzer: {regex}")
            return {"success": False, "error": "Expresión regular inválida."}

        try:
            nfa = regex_to_nfa_epsilon(regex)
            dfa = nfa_epsilon_to_dfa(nfa)

            log.info("Regex analizada y convertida a NFA/AFD correctamente.")

            return {
                "success": True,
                "regex": regex,
                "nfa_states": len(nfa.states),
                "dfa_states": len(dfa.states),
                "dfa": dfa.__dict__
            }
        except Exception as e:
            log.error(f"Error analizando regex: {e}")
            return {"success": False, "error": str(e)}