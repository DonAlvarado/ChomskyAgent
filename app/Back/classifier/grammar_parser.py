from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Iterable, Optional
import re
import uuid

from Back.utils.logger import get_logger

log = get_logger("GrammarParser")


@dataclass
class Grammar:
    id: str
    raw_rules: List[str]
    productions: Dict[str, List[str]]
    nonterminals: Set[str]
    terminals: Set[str]
    start_symbol: str
    metadata: Dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "raw_rules": self.raw_rules,
            "productions": self.productions,
            "nonterminals": sorted(self.nonterminals),
            "terminals": sorted(self.terminals),
            "start_symbol": self.start_symbol,
            "metadata": self.metadata,
        }


_ARROW = r"(->|→|::=|:)"
_RULE = re.compile(
    rf"^\s*(?P<lhs>.+?)\s*{_ARROW}\s*(?P<rhs>.+?)\s*$"
)


def _clean(line: str) -> str:
    if "//" in line:
        line = line.split("//", 1)[0]
    if "#" in line:
        line = line.split("#", 1)[0]
    return line.strip()


def _split(rhs: str) -> List[str]:
    return [x.strip() for x in rhs.split("|") if x.strip()]


def _tokens(rhs_alt: str) -> List[str]:
    rhs_alt = rhs_alt.strip()
    toks = []
    buf = ""

    for c in rhs_alt:
        if c.isupper():
            if buf:
                toks.append(buf)
                buf = ""
            toks.append(c)
        else:
            buf += c

    if buf:
        toks.append(buf)

    return toks




def _is_nt(sym: str) -> bool:
    return any(c.isupper() for c in sym)


def _eps(sym: str) -> Optional[str]:
    s = sym.lower().strip()
    if s in {"ε", "epsilon", "eps", "λ", "lambda"}:
        return None
    return sym


def parse_grammar(rules: Iterable[str], start_symbol: Optional[str] = None) -> Grammar:
    raw_rules: List[str] = []
    productions: Dict[str, List[str]] = {}
    nonterms: Set[str] = set()
    terms: Set[str] = set()
    first_lhs: Optional[str] = None

    for line in rules:
        if line is None:
            continue
        cleaned = _clean(str(line))
        if not cleaned:
            continue

        raw_rules.append(cleaned)
        m = _RULE.match(cleaned)
        if not m:
            log.error(f"Regla inválida detectada: '{cleaned}'")
            raise ValueError(f"Regla inválida: '{cleaned}'")

        lhs = m.group("lhs").strip()
        rhs = m.group("rhs").strip()
        if first_lhs is None:
            first_lhs = lhs

        nonterms.add(lhs)
        alts = _split(rhs)

        for alt in alts:
            productions.setdefault(lhs, []).append(alt)
            toks = _tokens(alt)
            for t in toks:
                norm = _eps(t)
                if norm is None:
                    continue
                if _is_nt(norm):
                    nonterms.add(norm)
                else:
                    terms.add(norm)

    if not raw_rules:
        raise ValueError("No hay reglas válidas.")

    start = start_symbol or first_lhs
    if start not in nonterms:
        nonterms.add(start)

    g = Grammar(
        id=str(uuid.uuid4()),
        raw_rules=raw_rules,
        productions=productions,
        nonterminals=nonterms,
        terminals=terms,
        start_symbol=start,
    )

    log.info(f"Gramática parseada con {len(g.productions)} no terminales y {len(g.terminals)} terminales.")
    return g
