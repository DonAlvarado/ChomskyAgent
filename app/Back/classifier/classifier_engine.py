from __future__ import annotations
from typing import List

from .grammar_parser import Grammar
from Back.utils.logger import get_logger

log = get_logger("ClassifierEngine")


def _tokens(rhs_alt: str) -> List[str]:
    rhs_alt = rhs_alt.strip()
    if " " in rhs_alt:
        return [t for t in rhs_alt.split(" ") if t]
    return list(rhs_alt)


def _is_nt(sym: str) -> bool:
    return any(c.isupper() for c in sym)


def _is_eps(sym: str) -> bool:
    s = sym.lower().strip()
    return s in {"ε", "epsilon", "eps", "λ", "lambda"}


def _is_regular_rhs(rhs_alt: str) -> bool:
    s = rhs_alt.strip()
    if _is_eps(s):
        return True

    toks = _tokens(s)

    if len(toks) == 1:
        # A -> a
        return not _is_nt(toks[0])

    if len(toks) == 2:
        # A -> aB
        return (not _is_nt(toks[0])) and _is_nt(toks[1])

    return False


def _all_regular(g: Grammar, steps: List[str]) -> bool:
    for lhs, alts in g.productions.items():
        if len(lhs) != 1 or not _is_nt(lhs):
            steps.append(f"'{lhs}' no es un solo no terminal, rompe Tipo 3.")
            return False
        for rhs in alts:
            if not _is_regular_rhs(rhs):
                steps.append(f"'{lhs} -> {rhs}' no cumple forma regular.")
                return False
    steps.append("Todas las producciones cumplen forma regular (Tipo 3).")
    return True


def _all_cfl(g: Grammar, steps: List[str]) -> bool:
    for lhs in g.productions.keys():
        if len(lhs) != 1 or not _is_nt(lhs):
            steps.append(f"'{lhs}' no es un solo no terminal, rompe Tipo 2.")
            return False
    steps.append("Todos los lados izquierdos son un solo no terminal (Tipo 2).")
    return True


def _all_context_sensitive(g: Grammar, steps: List[str]) -> bool:
    for lhs, alts in g.productions.items():
        for rhs in alts:
            s = rhs.strip()
            if _is_eps(s):
                continue
            if len(lhs) > len(s):
                steps.append(f"'{lhs} -> {rhs}' viola |α| ≤ |β|, rompe Tipo 1.")
                return False
    steps.append("Todas las producciones cumplen |α| ≤ |β| (Tipo 1).")
    return True


def classify_grammar(g: Grammar) -> Grammar:
    steps: List[str] = []
    gtype = "Tipo 0 (Recursivamente enumerable)"

    if _all_regular(g, steps):
        gtype = "Tipo 3 (Regular)"
    else:
        steps.append("No cumple restricciones de Tipo 3.")
        if _all_cfl(g, steps):
            gtype = "Tipo 2 (Libre de contexto)"
        else:
            steps.append("No cumple restricciones de Tipo 2.")
            if _all_context_sensitive(g, steps):
                gtype = "Tipo 1 (Sensible al contexto)"
            else:
                steps.append("No cumple restricciones de Tipo 1. Se clasifica como Tipo 0.")

    g.metadata["classification"] = {
        "type": gtype,
        "steps": steps,
    }

    log.info(f"Gramática clasificada como {gtype}")
    log.debug("Pasos de clasificación: " + " | ".join(steps))

    return g
