from __future__ import annotations
import random

from Back.utils.logger import get_logger

log = get_logger("ExampleGenerator")


REGULAR_PRODUCTIONS = [
    {"S": ["aA", "bB"], "A": ["aS", "a"], "B": ["bS", "b"]},
    {"S": ["0A", "1"], "A": ["1S", "ε"]},
]

CFL_PRODUCTIONS = [
    {"S": ["aSb", "ab"]},
    {"S": ["SS", "a"]},
]

REGEX_EXAMPLES = [
    "a(b|a)*",
    "(01)*1",
    "a*b*",
]


def random_regular_grammar():
    g = random.choice(REGULAR_PRODUCTIONS)
    log.debug(f"Gramática regular generada: {g}")
    return g


def random_cfl_grammar():
    g = random.choice(CFL_PRODUCTIONS)
    log.debug(f"Gramática CFL generada: {g}")
    return g


def random_regex():
    r = random.choice(REGEX_EXAMPLES)
    log.debug(f"Regex generada: {r}")
    return r


def generate(type_hint: str) -> dict:
    if type_hint == "regular":
        return {"productions": random_regular_grammar(), "type": "Tipo 3"}
    if type_hint == "cfl":
        return {"productions": random_cfl_grammar(), "type": "Tipo 2"}
    if type_hint == "regex":
        return {"regex": random_regex()}
    log.error(f"Tipo de ejemplo no reconocido: {type_hint}")
    return {"error": "tipo no reconocido"}
