import re

class ExplainableAI:
    # 1. Extracción de reglas de gramática
    def extract_rules(self, text: str):

        pattern = r"([A-Za-z][A-Za-z0-9_]*)\s*->\s*([A-Za-z0-9_()+*?|]+)"
        matches = re.findall(pattern, text)
        rules = []

        for left, right in matches:
            left = left.strip()
            right = right.strip()
            if left and right:
                rules.append((left, right))

        return rules

    # 2. Extracción de autómatas
    def extract_automaton_info(self, text: str):
        pattern = r"\(\s*(.*?)\s*,\s*(.*?)\s*\)\s*=\s*(\S+)"
        transitions = []

        for state, symbol, target in re.findall(pattern, text):
            transitions.append((state, symbol, target))

        return {"transitions": transitions}

    # 3. Extracción de regex
    def extract_regex_info(self, text: str):
        pattern = r"[A-Za-z0-9()*+?|]+"
        candidates = re.findall(pattern, text)

        candidates = [
            c for c in candidates
            if any(ch in c for ch in "|*+?()")
        ]

        if not candidates:
            return {"regex": None}

        candidates.sort(key=len, reverse=True)
        return {"regex": candidates[0]}

    # 4. Explicación extendida de una gramática analizada
    def explain_grammar(self, grammar_dict):
        gtype = grammar_dict.get("type", "Desconocido")
        steps = grammar_dict.get("steps", [])

        text = f"Esta gramática es clasificada como {gtype}. Razones:\n"
        for s in steps:
            text += f" - {s}\n"

        return text
