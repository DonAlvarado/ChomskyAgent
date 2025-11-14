from __future__ import annotations
from typing import Set, Tuple
from collections import deque

from Back.classifier.grammar_parser import Grammar
from Back.classifier.automata_parser import Automaton
from Back.utils.logger import get_logger

log = get_logger("EquivalenceChecker")

# Limite de longitud para comparar lenguajes L ≤ N
MAX_LEN = 6


def _is_terminal_string(s: str) -> bool:
    # asumimos: no terminal = mayúscula, terminal = lo demás
    return all(not c.isupper() for c in s)


def _normalize_eps(s: str) -> str:
    s = s.lower().strip()
    return "" if s in {"ε", "eps", "epsilon", "λ", "lambda"} else None


#   GRAMMARS
def generate_from_grammar(g: Grammar, max_len: int = MAX_LEN) -> Set[str]:
    """Genera todas las cadenas terminales de la gramática
    con longitud ≤ max_len, mediante BFS sobre derivaciones."""
    results: Set[str] = set()
    q = deque()

    # cadena inicial: símbolo de arranque
    q.append(g.start_symbol)
    visited = set([g.start_symbol])

    while q:
        sentential = q.popleft()

        # longitud de la parte terminal
        term_len = sum(1 for c in sentential if not c.isupper())
        if term_len > max_len:
            continue

        # si ya no hay no terminales, es cadena candidata
        if _is_terminal_string(sentential):
            results.add(sentential)
            continue

        # busca primer no terminal para expandir
        idx = None
        for i, c in enumerate(sentential):
            if c.isupper():
                idx = i
                break
        if idx is None:
            continue

        nt = sentential[idx]

        for rhs in g.productions.get(nt, []):
            eps_norm = _normalize_eps(rhs)
            if eps_norm is not None:
                repl = eps_norm 
            else:
                repl = rhs

            new_sent = sentential[:idx] + repl + sentential[idx + 1:]

            # pequeña poda para que no explote
            new_term_len = sum(1 for c in new_sent if not c.isupper())
            if new_term_len > max_len:
                continue

            if new_sent not in visited:
                visited.add(new_sent)
                q.append(new_sent)

    log.info(f"Lenguaje generado por gramática (≤ {max_len}): {sorted(results)}")
    return results


#   AUTOMATA
def generate_from_automaton(a: Automaton, max_len: int = MAX_LEN) -> Set[str]:
    """Genera todas las cadenas aceptadas por el autómata
    con longitud ≤ max_len."""
    results: Set[str] = set()
    q = deque()

    # estado, cadena_generada
    q.append((a.start, ""))

    visited: Set[Tuple[str, str]] = set()
    visited.add((a.start, ""))

    while q:
        state, s = q.popleft()

        if len(s) > max_len:
            continue

        if state in a.accept:
            results.add(s)

        # transiciones por símbolos
        for sym in a.alphabet:
            dsts = a.transitions.get(state, {}).get(sym, [])
            for dst in dsts:
                new_s = s + sym
                if len(new_s) > max_len:
                    continue
                key = (dst, new_s)
                if key not in visited:
                    visited.add(key)
                    q.append((dst, new_s))

        # transiciones epsilon
        eps_dsts = a.transitions.get(state, {}).get("ε", [])
        for dst in eps_dsts:
            key = (dst, s)
            if key not in visited:
                visited.add(key)
                q.append((dst, s))

    log.info(f"Lenguaje generado por autómata (≤ {max_len}): {sorted(results)}")
    return results


#   API PÚBLICA

def equivalent(obj1, obj2, max_len: int = MAX_LEN):
    # Gramática vs Gramática
    if isinstance(obj1, Grammar) and isinstance(obj2, Grammar):
        L1 = generate_from_grammar(obj1, max_len)
        L2 = generate_from_grammar(obj2, max_len)

        eq = (L1 == L2)
        diff1 = sorted(L1 - L2)
        diff2 = sorted(L2 - L1)

        explanation = {
            "type": "grammar",
            "max_len": max_len,
            "equivalent": eq,
            "L1": sorted(L1),
            "L2": sorted(L2),
            "L1_minus_L2": diff1,
            "L2_minus_L1": diff2,
        }

        return explanation

    # Autómata vs Automata
    if isinstance(obj1, Automaton) and isinstance(obj2, Automaton):
        L1 = generate_from_automaton(obj1, max_len)
        L2 = generate_from_automaton(obj2, max_len)

        eq = (L1 == L2)
        diff1 = sorted(L1 - L2)
        diff2 = sorted(L2 - L1)

        explanation = {
            "type": "automaton",
            "max_len": max_len,
            "equivalent": eq,
            "L1": sorted(L1),
            "L2": sorted(L2),
            "L1_minus_L2": diff1,
            "L2_minus_L1": diff2,
        }

        return explanation

    raise ValueError("Solo se pueden comparar dos gramáticas o dos autómatas del mismo tipo.")