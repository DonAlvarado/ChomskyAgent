from .reasoner import Reasoner
from .action_manager import ActionManager


class Chatbot:
    def __init__(self):
        self.reasoner = Reasoner()
        self.action_manager = ActionManager()
        self.history = []

    def handle(self, message: str) -> str:
        self.history.append(("user", message))

        info = self.reasoner.process(message)
        intent = info["intent"]
        action = info["action"]

        # Acciones principales delegadas a ActionManager
        result = self.action_manager.execute(action, message)

        # Si es smalltalk o no hay acción válida
        if result is None:
            result = self.smalltalk_reply(message)

        self.history.append(("agent", result))
        return result

    def smalltalk_reply(self, msg: str) -> str:
        msg = msg.lower()

        if "hola" in msg or "buenas" in msg:
            return "Hola, ¿qué necesitas analizar?"
        if "gracias" in msg:
            return "De nada."
        if "qué tal" in msg or "como estas" in msg:
            return "Listo para seguir trabajando con gramáticas y autómatas."

        return "¿Deseas analizar algo o generar una explicación?"
