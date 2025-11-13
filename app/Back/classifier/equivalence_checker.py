from __future__ import annotations
from typing import Dict, Set

from Back.classifier.converter import (
    nfa_epsilon_to_dfa,
    dfa_to_regular_grammar,
    grammar_to_afd
)

# Minimización AFD

def minimize_dfa(dfa):
    partitions = [set(dfa.accept), set(dfa.states - dfa.accept)]
    stable = False

    while not stable:
        stable = True
        new_partitions = []

        for group in partitions:
            rep = next(iter(group))
            buckets: Dict[str, Set[str]] = {}

            for state in group:
                signature = []
                for sym in dfa.alphabet:
                    dst = dfa.transitions.get(state, {}).get(sym)
                    part_id = next(
                        (i for i, p in enumerate(partitions) if dst in p),
                        None
                    )
                    signature.append(part_id)
                signature = tuple(signature)
                buckets.setdefault(signature, set()).add(state)

            for b in buckets.values():
                new_partitions.append(b)

            if len(buckets.values()) > 1:
                stable = False

        partitions = new_partitions

    new_states = {f"M{i}": p for i, p in enumerate(partitions)}
    inv = {frozenset(v): k for k, v in new_states.items()}

    trans = {}
    for nid, group in new_states.items():
        rep = next(iter(group))
        trans[nid] = {}
        for sym in dfa.alphabet:
            dst = dfa.transitions.get(rep, {}).get(sym)
            if dst:
                target = next(p for p in partitions if dst in p)
                trans[nid][sym] = inv[frozenset(target)]

    start_group = next(p for p in partitions if dfa.start in p)
    start = inv[frozenset(start_group)]

    accept = set()
    for nid, group in new_states.items():
        if group & dfa.accept:
            accept.add(nid)

    from app.Back.classifier.converter import DFA
    return DFA(
        states=set(new_states.keys()),
        alphabet=dfa.alphabet,
        start=start,
        accept=accept,
        transitions=trans
    )

# Convertir a AFD minimizado

def to_minimized_dfa(obj):
    # Ya es AFD
    if hasattr(obj, "transitions") and isinstance(obj.transitions, dict):
        dfa = obj
        return minimize_dfa(dfa)

    # Es AFN o AFN-e
    if hasattr(obj, "alphabet") and isinstance(obj.accept, set):
        from app.Back.classifier.automata_parser import detect_type
        from app.Back.classifier.converter import regex_to_nfa_epsilon
        typ = detect_type(obj)
        if typ in ("AFN", "AFN-ε"):
            dfa = nfa_epsilon_to_dfa(obj)
            return minimize_dfa(dfa)

    # Es gramática
    if hasattr(obj, "productions"):
        dfa = grammar_to_afd(obj)
        return minimize_dfa(dfa)

    raise ValueError("Objeto no convertible a AFD minimizado.")

# Equivalencia

def equivalent(obj1, obj2) -> bool:
    d1 = to_minimized_dfa(obj1)
    d2 = to_minimized_dfa(obj2)

    # Comparación directa del AFD minimizado
    return (
        d1.alphabet == d2.alphabet and
        len(d1.states) == len(d2.states) and
        d1.start == d2.start and
        d1.accept == d2.accept and
        d1.transitions == d2.transitions
    )
