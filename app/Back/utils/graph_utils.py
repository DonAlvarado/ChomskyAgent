from graphviz import Digraph

def create_graph(rankdir="LR"):
    g = Digraph()
    g.attr(rankdir=rankdir)
    return g

def export_svg(dot: Digraph) -> str:
    return dot.pipe(format="svg").decode("utf-8")
