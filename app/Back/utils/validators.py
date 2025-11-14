import re

def is_valid_regex(regex: str) -> bool:
    if not isinstance(regex, str) or not regex.strip():
        return False

    try:
        re.compile(regex)
        return True
    except Exception:
        return False


def is_valid_grammar(rules: list[str]) -> bool:
    if not rules:
        return False

    pattern = re.compile(r"^[A-Z]\s*->\s*[a-zA-Z0-9ε| ]+$")

    return all(pattern.match(rule.strip()) for rule in rules)


def is_valid_automaton(data: dict) -> bool:
    required = ["states", "alphabet", "start", "accept", "transitions"]

    if not all(k in data for k in required):
        return False

    if data["start"] not in data["states"]:
        return False

    if not set(data["accept"]).issubset(set(data["states"])):
        return False

    return True
