# memory.py
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Turn:
    role: str
    text: str
    meta: Dict[str, Any] | None = None


class SessionMemory:
    """
    Guarda los últimos N turnos del chat.
    No persistente (pero puedes agregarlo después).
    """

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.turns: List[Turn] = []

    def add_turn(self, role: str, text: str, meta: Dict[str, Any] | None = None):
        self.turns.append(Turn(role=role, text=text, meta=meta or {}))

        # si excede límite, recorta por izquierda
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def as_list(self) -> List[Dict[str, Any]]:
        return [t.__dict__ for t in self.turns]
