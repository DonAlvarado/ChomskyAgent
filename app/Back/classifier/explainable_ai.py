from __future__ import annotations
from typing import Dict, Any, List


class ExplainableAI:

    def explain_grammar_classification(self, grammar) -> Dict[str, Any]:
        meta = grammar.metadata.get("classification", {})
        gtype = meta.get("type", "Desconocido")
        steps = meta.get("steps", [])

        return {
            "type": gtype,
            "steps": steps
        }

    def explain_automaton(self, automaton) -> Dict[str, Any]:
        t = automaton.metadata.get("type") or "Desconocido"

        if t == "AFD":
            detail = "El autómata es determinista porque cada estado tiene a lo sumo una transición por símbolo."
        elif t == "AFN":
            detail = "El autómata es no determinista porque algún estado tiene múltiples transiciones para el mismo símbolo."
        elif t == "AFN-ε":
            detail = "El autómata es no determinista con epsilon porque existen transiciones ε."
        else:
            detail = "No se pudo determinar el tipo del autómata."

        return {
            "type": t,
            "explanation": detail
        }

    def explain_regex_conversion(self, regex: str, nfa, dfa) -> Dict[str, Any]:
        return {
            "regex": regex,
            "steps": [
                "Se analizó la expresión regular.",
                "Se construyó un AFN-ε mediante el algoritmo de Thompson.",
                "Se aplicó clausura-ε y construcción por subconjuntos para obtener el AFD."
            ],
            "nfa_states": len(nfa.states),
            "dfa_states": len(dfa.states)
        }

    def suggest_improvements(self, grammar) -> List[str]:
        tips = []

        for A, alts in grammar.productions.items():
            for rhs in alts:
                if len(rhs) > 3:
                    tips.append(f"La producción '{A} -> {rhs}' podría reescribirse en varias reglas más simples.")
                if rhs == "ε" and A == grammar.start_symbol:
                    tips.append("Considerar evitar ε-producciones en el símbolo inicial.")

        if not tips:
            tips.append("La gramática está en buena forma general.")

        return tips

    def explain_conversion_steps(self, steps: List[str]) -> Dict[str, Any]:
        return {
            "steps": steps
        }
