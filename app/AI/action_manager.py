import requests


class ActionManager:
    def __init__(self):
        self.base = "http://localhost:5000"
        self.last_rules = None
        self.last_regex = None
        self.last_automaton = None

    def execute(self, action: str, message: str):
        if action == "ANALYZE_GRAMMAR":
            return self._analyze_grammar(message)
        if action == "EXPLAIN_GRAMMAR":
            return self._explain_grammar()
        if action == "CONVERT_REPRESENTATION":
            return self._convert(message)
        if action == "GENERATE_EXAMPLE":
            return self._generate_example(message)
        if action == "GENERATE_PDF":
            return self._generate_pdf()
        if action == "START_TUTOR_MODE":
            return self._tutor(message)
        if action == "COMPARE_GRAMMARS":
            return self._compare(message)

        return None

    def _analyze_grammar(self, text):
        rules = [r.strip() for r in text.split("\n") if "→" in r or "->" in r]
        if not rules:
            return "No detecté reglas válidas."

        self.last_rules = rules

        try:
            r = requests.post(
                f"{self.base}/api/grammar/analyze",
                json={"rules": rules}
            ).json()
        except:
            return "Error comunicando con /api/grammar/analyze"

        if not r.get("success"):
            return r.get("error", "Error analizando la gramática.")

        g = r.get("classification", {})
        gtype = g.get("type", "desconocido")

        return f"Gramática analizada. Tipo detectado: {gtype}"

    def _explain_grammar(self):
        if not self.last_rules:
            return "Primero analiza una gramática."

        try:
            r = requests.post(
                f"{self.base}/api/agent/message",
                json={"message": "analiza esta gramática", "rules": self.last_rules}
            ).json()
        except:
            return "Error comunicando con /api/agent/message"

        return r.get("reply", "Sin explicación disponible.")

    def _convert(self, text):
        if "regex" in text.lower():
            regex = text.split("regex")[-1].strip()
        else:
            regex = text.strip()

        self.last_regex = regex

        try:
            r = requests.post(
                f"{self.base}/api/converter/regex2afd",
                json={"regex": regex}
            ).json()
        except:
            return "Error comunicando con /converter/regex2afd"

        if not r.get("success"):
            return r.get("error", "Error en conversión.")

        afd = r.get("afd", {})
        return f"Conversión realizada. AFD con {len(afd.get('states', []))} estados."

    def _generate_example(self, msg):
        try:
            r = requests.post(
                f"{self.base}/api/tutor/question",
                json={"difficulty": "basic"}
            ).json()
        except:
            return "Error comunicando con /tutor/question"

        if not r.get("success"):
            return "No pude generar un ejemplo."

        return f"Ejercicio generado: {r.get('question')}"

    def _generate_pdf(self):
        if self.last_rules:
            payload = {"type": "grammar", "rules": self.last_rules, "title": "Reporte Gramática"}
        elif self.last_regex:
            payload = {"type": "regex", "regex": self.last_regex, "title": "Reporte Regex"}
        elif self.last_automaton:
            payload = {"type": "automaton", "automaton": self.last_automaton, "title": "Reporte Autómata"}
        else:
            return "No existe ningún análisis previo."

        try:
            r = requests.post(
                f"{self.base}/api/report/generate",
                json=payload
            ).json()
        except:
            return "Error comunicando con /report/generate"

        if not r.get("success"):
            return r.get("error", "Error generando PDF.")

        return f"Reporte generado: {r.get('file')}"

    def _tutor(self, msg):
        try:
            r = requests.post(
                f"{self.base}/api/tutor/question",
                json={"difficulty": "basic"}
            ).json()
        except:
            return "Error comunicando con /tutor/question"

        if not r.get("success"):
            return r.get("error", "Error generando pregunta.")

        q = r["question"]
        return f"Pregunta: {q}"

    def _compare(self, msg):
        return "Aún no implementado."
