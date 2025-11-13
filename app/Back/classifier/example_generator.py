from __future__ import annotations
import random


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
    return random.choice(REGULAR_PRODUCTIONS)


def random_cfl_grammar():
    return random.choice(CFL_PRODUCTIONS)


def random_regex():
    return random.choice(REGEX_EXAMPLES)


def generate(type_hint: str) -> dict:
    if type_hint == "regular":
        return {"productions": random_regular_grammar(), "type": "Tipo 3"}
    if type_hint == "cfl":
        return {"productions": random_cfl_grammar(), "type": "Tipo 2"}
    if type_hint == "regex":
        return {"regex": random_regex()}
    return {"error": "tipo no reconocido"}
