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


class GrammarAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        rules = data.get("rules") or []
        start = data.get("start_symbol")

        g = parse_grammar(rules, start)
        g = classify_grammar(g)

        return {
            "success": True,
            "grammar": g.to_dict(),
            "classification": g.metadata.get("classification")
        }


class AutomataAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        a = parse_automaton(data)
        t = detect_type(a)

        return {
            "success": True,
            "automaton": a.to_dict(),
            "type": t
        }


class RegexAnalyzer(IAnalyzer):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        regex = data.get("regex", "")
        nfa = regex_to_nfa_epsilon(regex)
        dfa = nfa_epsilon_to_dfa(nfa)

        return {
            "success": True,
            "regex": regex,
            "nfa_states": len(nfa.states),
            "dfa_states": len(dfa.states),
            "dfa": dfa.__dict__
        }
