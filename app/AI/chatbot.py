# chatbot.py

from AI.reasoner import Reasoner, Intent
from AI.action_manager import ActionManager
from AI.memory import SessionMemory


class Chatbot:
    """
    Maneja la interacción entre usuario, Reasoner e ActionManager.
    """

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.reasoner = Reasoner()
        self.actions = ActionManager(base_url=base_url)
        self.memory = SessionMemory(max_turns=20)

    def handle_message(self, message: str):
        print("[DEBUG] Chatbot.handle_message EJECUTADO")

        # 1. Guarda turno del usuario
        self.memory.add_turn("user", message)

        # 2. Detecta intención
        intent: Intent = self.reasoner.infer_intent(message)

        # 3. Ejecuta acción correspondiente
        raw_result = self.actions.execute(intent.action, message)

        # 4. Formatea la respuesta
        reply_text = self.reasoner.format_reply(intent, raw_result)

        # 5. Guarda turno del agente
        self.memory.add_turn("agent", reply_text, {"intent": intent.action})

        # 6. Devuelve payload para endpoint Flask
        return {
            "reply": reply_text,
            "intent": intent.action,
            "raw_result": raw_result
        }
