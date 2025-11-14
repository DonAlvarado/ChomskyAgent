import os
import joblib


class Reasoner:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base, "intent_model.pkl")

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = None

    # Predicción con ML
    def classify_intent(self, message: str) -> str:
        if not self.model:
            return self.rule_fallback(message)
        return self.model.predict([message])[0]

    # Reglas básicas si no existe modelo
    def rule_fallback(self, msg: str) -> str:
        msg = msg.lower()

        if "analiz" in msg or "clasific" in msg:
            return "analyze"
        if "explica" in msg:
            return "explain"
        if "convierte" in msg or "regex" in msg:
            return "convert"
        if "ejemplo" in msg or "genera" in msg:
            return "example"
        if "pdf" in msg or "reporte" in msg:
            return "pdf"
        if "quiz" in msg or "practicar" in msg:
            return "tutor"
        if "compara" in msg or "equivalenc" in msg:
            return "compare"

        return "smalltalk"

    # Mapeo intención → acción
    def decide_action(self, intent: str) -> str:
        mapping = {
            "analyze": "ANALYZE_GRAMMAR",
            "explain": "EXPLAIN_GRAMMAR",
            "convert": "CONVERT_REPRESENTATION",
            "example": "GENERATE_EXAMPLE",
            "pdf": "GENERATE_PDF",
            "tutor": "START_TUTOR_MODE",
            "compare": "COMPARE_GRAMMARS",
            "smalltalk": "SMALLTALK"
        }
        return mapping.get(intent, "UNKNOWN")

    # Proceso principal
    def process(self, message: str) -> dict:
        intent = self.classify_intent(message)
        action = self.decide_action(intent)

        return {
            "intent": intent,
            "action": action
        }
