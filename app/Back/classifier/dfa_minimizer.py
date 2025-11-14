from typing import Dict, Set
from Back.classifier.converter import DFA
from Back.utils.logger import get_logger

log = get_logger("DfaMinimizer")


def minimize_dfa(dfa: DFA) -> DFA:
    states = dfa.states
    alphabet = dfa.alphabet
    transitions = dfa.transitions
    accept = dfa.accept
    start = dfa.start

    original_states = len(states)

    P = [set(accept), set(states) - set(accept)]
    W = [set(accept)]

    while W:
        A = W.pop()
        for c in alphabet:
            X = {q for q in states if transitions.get(q, {}).get(c) in A}
            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    new_P.append(inter)
                    new_P.append(diff)
                    if Y in W:
                        W.remove(Y)
                        W.append(inter)
                        W.append(diff)
                    else:
                        if len(inter) <= len(diff):
                            W.append(inter)
                        else:
                            W.append(diff)
                else:
                    new_P.append(Y)
            P = new_P

    block_map = {}
    new_states = []
    for idx, block in enumerate(P):
        name = f"Q{idx}"
        new_states.append(name)
        for s in block:
            block_map[s] = name

    new_start = block_map[start]
    new_accept = {block_map[s] for s in accept}

    new_trans = {q: {} for q in new_states}
    for old in states:
        qnew = block_map[old]
        for sym, dst in transitions.get(old, {}).items():
            new_trans[qnew][sym] = block_map[dst]

    minimized = DFA(
        states=set(new_states),
        alphabet=alphabet,
        start=new_start,
        accept=new_accept,
        transitions=new_trans
    )

    log.info(f"AFD minimizado: {original_states} → {len(minimized.states)} estados.")
    return minimized
