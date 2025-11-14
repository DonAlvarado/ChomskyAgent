from __future__ import annotations
from typing import Any
from graphviz import Digraph

from Back.interfaces.IVisualizer import IVisualizer
from Back.utils.graph_utils import create_graph
from Back.utils.logger import get_logger

log = get_logger("Visualizer")


class DFAVisualizer(IVisualizer):
    def visualize(self, dfa: Any) -> str:
        # Devolvemos DOT (g.source), NO SVG
        g: Digraph = create_graph("LR")
        g.node("", shape="none")

        # estados
        for q in dfa.states:
            shape = "doublecircle" if q in dfa.accept else "circle"
            g.node(q, shape=shape)

        # flecha inicial
        g.edge("", dfa.start)

        # transiciones
        for q, moves in dfa.transitions.items():
            for sym, dst_list in moves.items():
                # AFD: podría venir como lista o string
                if isinstance(dst_list, list) and len(dst_list) == 1:
                    dst = dst_list[0]
                else:
                    dst = dst_list
                g.edge(q, dst, label=sym)

        dot = g.source
        log.debug("DOT generado para DFA.")
        return dot


class NFAVisualizer(IVisualizer):
    def visualize(self, nfa: Any) -> str:
        g: Digraph = create_graph("LR")
        g.node("", shape="none")

        for q in nfa.states:
            shape = "doublecircle" if q in nfa.accept else "circle"
            g.node(q, shape=shape)

        g.edge("", nfa.start)

        for q, moves in nfa.transitions.items():
            for sym, dsts in moves.items():
                for dst in dsts:
                    g.edge(q, dst, label=sym)

        dot = g.source
        log.debug("DOT generado para NFA.")
        return dot


class GrammarVisualizer(IVisualizer):
    def visualize(self, grammar: Any) -> str:
        g: Digraph = create_graph("LR")
        g.node("", shape="none")

        for nt in grammar.nonterminals:
            shape = "doublecircle" if nt == grammar.start_symbol else "circle"
            g.node(nt, shape=shape)

        g.edge("", grammar.start_symbol)

        for A, alts in grammar.productions.items():
            for rhs in alts:
                if rhs == "ε":
                    g.node(f"{A}_eps", shape="point", label="ε")
                    g.edge(A, f"{A}_eps")
                    continue

                toks = list(rhs)
                if len(toks) == 1:
                    t = toks[0]
                    g.node(f"{A}_{t}", shape="box", label=t)
                    g.edge(A, f"{A}_{t}")
                elif len(toks) == 2:
                    a, B = toks
                    g.edge(A, B, label=a)

        dot = g.source
        log.debug("DOT generado para gramática.")
        return dot
