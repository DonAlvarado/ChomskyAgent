from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional 
import uuid


# Estructuras internas

@dataclass
class NFA:
    states: Set[str]
    alphabet: Set[str]
    start: str
    accept: Set[str]
    transitions: Dict[str, Dict[str, List[str]]]


@dataclass
class DFA:
    states: Set[str]
    alphabet: Set[str]
    start: str
    accept: Set[str]
    transitions: Dict[str, Dict[str, str]]


# Regex → AFN-ε (Thompson)

class _StackItem:
    def __init__(self, start, end):
        self.start = start
        self.end = end


def regex_to_nfa_epsilon(regex: str) -> NFA:
    # Algoritmo de Thompson simplificado (solo (), *, |, concatenación)
    postfix = _regex_to_postfix(regex)
    return _postfix_to_nfa(postfix)


def _regex_to_postfix(regex: str) -> str:
    # Shunting-yard minimal
    prec = {"*": 3, ".": 2, "|": 1}
    out = []
    stack = []

    # Insertar operador explícito de concatenación "."
    explicit = ""
    prev = ""
    for c in regex:
        if prev and (prev.isalnum() or prev == ")" or prev == "*") and (c.isalnum() or c == "("):
            explicit += "." + c
        else:
            explicit += c
        prev = c
    regex = explicit

    for c in regex:
        if c.isalnum():
            out.append(c)
        elif c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != "(" and prec.get(stack[-1], 0) >= prec[c]:
                out.append(stack.pop())
            stack.append(c)

    while stack:
        out.append(stack.pop())

    return "".join(out)


def _postfix_to_nfa(postfix: str) -> NFA:
    states_count = 0

    def new_state():
        nonlocal states_count
        s = f"s{states_count}"
        states_count += 1
        return s

    stack = []
    alphabet = set()

    for c in postfix:
        if c.isalnum():
            alphabet.add(c)
            s1, s2 = new_state(), new_state()
            trans = {
                s1: {c: [s2]},
                s2: {}
            }
            stack.append(_StackItem(s1, s2))
            stack[-1].transitions = trans

        elif c == ".":
            b = stack.pop()
            a = stack.pop()
            # conectar a.end → b.start por epsilon
            a.transitions[a.end] = {"ε": [b.start]}
            # unir transiciones
            merged = {**a.transitions}
            for k, v in b.transitions.items():
                merged[k] = v
            item = _StackItem(a.start, b.end)
            item.transitions = merged
            stack.append(item)

        elif c == "|":
            b = stack.pop()
            a = stack.pop()
            s_start, s_end = new_state(), new_state()
            merged = {
                s_start: {"ε": [a.start, b.start]},
                a.end: {"ε": [s_end]},
                b.end: {"ε": [s_end]},
            }
            for T in (a.transitions, b.transitions):
                for k, v in T.items():
                    merged[k] = v
            item = _StackItem(s_start, s_end)
            item.transitions = merged
            stack.append(item)

        elif c == "*":
            a = stack.pop()
            s_start, s_end = new_state(), new_state()
            merged = {
                s_start: {"ε": [a.start, s_end]},
                a.end: {"ε": [a.start, s_end]},
            }
            for k, v in a.transitions.items():
                merged[k] = v
            item = _StackItem(s_start, s_end)
            item.transitions = merged
            stack.append(item)

    item = stack.pop()

    # Normalización
    states = set(item.transitions.keys())
    for t in item.transitions.values():
        for lst in t.values():
            for x in lst:
                states.add(x)

    return NFA(
        states=states,
        alphabet=alphabet,
        start=item.start,
        accept={item.end},
        transitions=item.transitions
    )


# AFN-ε → AFD

def _epsilon_closure(nfa: NFA, states: Set[str]) -> Set[str]:
    stack = list(states)
    closure = set(states)

    while stack:
        s = stack.pop()
        if "ε" in nfa.transitions.get(s, {}):
            for nxt in nfa.transitions[s]["ε"]:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
    return closure


def nfa_epsilon_to_dfa(nfa: NFA) -> DFA:
    start = frozenset(_epsilon_closure(nfa, {nfa.start}))
    pending = [start]
    visited = set()
    d_states: Set[frozenset] = set([start])
    d_trans: Dict[frozenset, Dict[str, frozenset]] = {}

    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)

        d_trans[current] = {}

        for sym in nfa.alphabet:
            move = set()
            for s in current:
                if sym in nfa.transitions.get(s, {}):
                    for nxt in nfa.transitions[s][sym]:
                        move.add(nxt)

            closure = _epsilon_closure(nfa, move)
            if not closure:
                continue

            f = frozenset(closure)
            d_trans[current][sym] = f
            if f not in d_states:
                d_states.add(f)
                pending.append(f)

    # AFD resultante
    str_states = {f"D{i}": st for i, st in enumerate(d_states)}
    inv = {v: k for k, v in str_states.items()}

    det_trans = {}
    for fset, moves in d_trans.items():
        det_trans[inv[fset]] = {}
        for sym, dst in moves.items():
            det_trans[inv[fset]][sym] = inv[dst]

    start_id = inv[start]
    accept_ids = {sid for sid, fset in str_states.items() if fset & nfa.accept}

    return DFA(
        states=set(str_states.keys()),
        alphabet=nfa.alphabet,
        start=start_id,
        accept=accept_ids,
        transitions=det_trans
    )


# AFD → Gramática Regular

def dfa_to_regular_grammar(dfa: DFA) -> Dict[str, List[str]]:
    G = {}
    for q in dfa.states:
        G[q] = []
        for sym, dst in dfa.transitions.get(q, {}).items():
            G[q].append(sym + dst)
        if q in dfa.accept:
            G[q].append("ε")
    return G


# Gramática Regular → AFD

def grammar_to_afd(grammar) -> DFA:
    states = set(grammar.nonterminals)
    alphabet = set(grammar.terminals)
    start = grammar.start_symbol
    accept = set()

    trans = {}
    for A, alts in grammar.productions.items():
        trans[A] = {}
        for rhs in alts:
            if rhs == "ε":
                accept.add(A)
                continue
            toks = list(rhs)
            if len(toks) == 1:
                a = toks[0]
                accept.add(A)
            elif len(toks) == 2:
                a, B = toks
                trans[A][a] = B

    return DFA(
        states=states,
        alphabet=alphabet,
        start=start,
        accept=accept,
        transitions=trans
    )
