import requests
from Back.classifier.explainable_ai import ExplainableAI


class ActionManager:
    def __init__(self, base_url: str = "http://localhost:5000"):
        # Base de la API Flask
        self.base = base_url

        # Últimos artefactos analizados (para PDF / modo explicación)
        self.last_rules = None
        self.last_start_symbol = None
        self.last_automaton = None
        self.last_regex = None
        self.last_question = None
        self.last_grammar_classification = None

        # Módulo de IA explicativa local (no LLM)
        self.xai = ExplainableAI()

    # 1) GRAMÁTICAS
    def _analyze_grammar(self, message: str):
        try:
            rule_tuples = self.xai.extract_rules(message)
            rules = [f"{l} -> {r}" for (l, r) in rule_tuples]

            if not rules:
                return {"success": False, "error": "No detecté reglas válidas."}

            start_symbol = rules[0].split("->")[0].strip()

            payload = {
                "rules": rules,
                "start_symbol": start_symbol
            }

            print("[POST] /api/grammar/analyze :", payload)

            response = requests.post(f"{self.base}/api/grammar/analyze", json=payload)
            data = self.safe_json(response)

            if data.get("success"):
                self.last_rules = rules
                self.last_start_symbol = start_symbol
                self.last_grammar_classification = data.get("classification")

            return data

        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    def explain_last_grammar(self):
        if not self.last_grammar_classification:
            return {
                "success": False,
                "error": "No tengo una gramática previa analizada para explicar."
            }

        try:
            explanation = self.xai.explain_grammar(self.last_grammar_classification)
            return {
                "success": True,
                "explanation": explanation
            }
        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # 2) AUTÓMATAS
    def analyze_automaton(self, message: str):
        try:
            trans_raw = self.xai.extract_automaton_info(message)
            triples = trans_raw.get("transitions", [])

            if not triples:
                return {"success": False, "error": "No detecté transiciones válidas."}

            states = set()
            alphabet = set()
            transitions = {}

            for src, sym, dst in triples:
                src = src.strip()
                dst = dst.strip()
                sym = sym.strip()

                if not src or not dst or not sym:
                    continue

                states.add(src)
                states.add(dst)
                alphabet.add(sym)

                if src not in transitions:
                    transitions[src] = {}
                transitions[src][sym] = [dst]

            if not states:
                return {"success": False, "error": "No se pudieron construir estados válidos."}

            states_list = sorted(states)
            start = states_list[0]
            accept = [states_list[-1]]

            automaton = {
                "states": states_list,
                "alphabet": sorted(alphabet),
                "start": start,
                "accept": accept,
                "transitions": transitions
            }

            r = requests.post(f"{self.base}/api/automata/analyze", json=automaton)
            data = self.safe_json(r)

            if data.get("success"):
                auto_dict = data.get("automaton", automaton)
                auto_dict["detected_type"] = data.get("type", "Desconocido")
                self.last_automaton = auto_dict

            return data

        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # 3) REGEX → AFD
    def convert_regex(self, message: str):
        try:
            regex_info = self.xai.extract_regex_info(message)
            regex = regex_info.get("regex") if isinstance(regex_info, dict) else None

            if not regex:
                return {"success": False, "error": "No detecté expresión regular."}

            self.last_regex = regex
            payload = {"regex": regex}

            r = requests.post(f"{self.base}/api/converter/regex2afd", json=payload)
            return self.safe_json(r)

        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # 4) TUTOR
    def tutor_question(self):
        try:
            r = requests.post(
                f"{self.base}/api/tutor/question",
                json={"difficulty": "basic"}
            )
            data = self.safe_json(r)
            if data.get("success"):
                self.last_question = data
            return data
        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    def tutor_check(self, message: str):
        if not self.last_question:
            return {
                "success": False,
                "error": "No tengo una pregunta activa del tutor."
            }

        answer = message.strip()
        if not answer:
            return {
                "success": False,
                "error": "Necesito que me des una respuesta."
            }

        payload = {
            "question": self.last_question.get("question", ""),
            "answer": answer,
            "type": self.last_question.get("type", "basic")
        }

        try:
            r = requests.post(f"{self.base}/api/tutor/check", json=payload)
            return self.safe_json(r)
        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # 5) PDF
    def generate_pdf(self):
        try:
            if self.last_rules:
                payload = {
                    "type": "grammar",
                    "rules": self.last_rules,
                    "start_symbol": self.last_start_symbol or (
                        self.last_rules[0].split("->")[0].strip()
                        if self.last_rules else None
                    )
                }
            elif self.last_automaton:
                payload = {"type": "automaton", "automaton": self.last_automaton}
            elif self.last_regex:
                payload = {"type": "regex", "regex": self.last_regex}
            else:
                return {
                    "success": False,
                    "error": "No tengo información para generar un PDF."
                }

            r = requests.post(f"{self.base}/api/report/generate", json=payload)
            return self.safe_json(r)

        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # 6) EJECUTOR PRINCIPAL
    def execute(self, action: str, message: str):
        try:
            if action == "ANALYZE_GRAMMAR":
                return self._analyze_grammar(message)

            if action == "EXPLAIN_GRAMMAR":
                return self.explain_last_grammar()

            if action == "ANALYZE_AUTOMATON":
                return self.analyze_automaton(message)

            if action == "CONVERT_REPRESENTATION":
                return self.convert_regex(message)

            if action == "TUTOR_QUESTION":
                return self.tutor_question()

            if action == "TUTOR_CHECK":
                return self.tutor_check(message)

            if action == "GENERATE_PDF":
                return self.generate_pdf()

            return {"success": False, "error": "Acción no implementada."}

        except Exception as e:
            return {"success": False, "error": f"Excepción interna: {e}"}

    # Helper: JSON seguro
    def safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return {
                "success": False,
                "error": f"Respuesta no válida del servidor ({response.status_code})."
            }
