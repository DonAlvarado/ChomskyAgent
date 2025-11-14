from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

from Back.utils.validators import is_valid_automaton
from Back.utils.logger import get_logger

log = get_logger("AutomataParser")


@dataclass
class Automaton:
    id: str
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[str, Dict[str, List[str]]]
    start: str
    accept: Set[str]
    metadata: Dict[str, object] = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "states": sorted(self.states),
            "alphabet": sorted(self.alphabet),
            "transitions": self.transitions,
            "start": self.start,
            "accept": sorted(self.accept),
            "metadata": self.metadata,
        }


def parse_automaton(data: dict) -> Automaton:
    if not is_valid_automaton(data):
        log.error("Estructura básica de autómata inválida.")
        raise ValueError("Formato de autómata inválido.")

    states = set(data.get("states") or [])
    alphabet = set(data.get("alphabet") or [])
    start = data.get("start")
    accept = set(data.get("accept") or [])
    raw_trans = data.get("transitions") or {}

    if not states:
        raise ValueError("El autómata no tiene estados.")
    if start not in states:
        raise ValueError("El estado inicial no está en el conjunto de estados.")

    trans: Dict[str, Dict[str, List[str]]] = {}

    for s, moves in raw_trans.items():
        if s not in states:
            raise ValueError(f"Estado inválido en transiciones: '{s}'")
        trans[s] = {}

        for sym, dst in moves.items():
            if sym != "ε" and sym not in alphabet:
                raise ValueError(f"Símbolo inválido: '{sym}'")

            if isinstance(dst, str):
                dst_list = [dst]
            else:
                dst_list = list(dst)

            for d in dst_list:
                if d not in states:
                    raise ValueError(f"Destino inválido: '{d}' en transición '{s}'")

            trans[s][sym] = dst_list

    import uuid
    a = Automaton(
        id=str(uuid.uuid4()),
        states=states,
        alphabet=alphabet,
        transitions=trans,
        start=start,
        accept=accept,
    )
    log.info(f"Autómata parseado correctamente con {len(states)} estados.")
    return a


def detect_type(a: Automaton) -> str:
    for s, moves in a.transitions.items():
        for sym, dst in moves.items():
            if sym == "ε":
                return "AFN-ε"
            if len(dst) > 1:
                return "AFN"
    return "AFD"
