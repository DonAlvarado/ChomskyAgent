from flask import Blueprint, request, jsonify
import os

from Back.classifier.pdf_reporter import PDFReporter
from Back.classifier.visualizer import (
    GrammarVisualizer,
    DFAVisualizer,
    NFAVisualizer
)
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.automata_parser import parse_automaton
from Back.classifier.converter import (
    regex_to_nfa_epsilon,
    nfa_epsilon_to_dfa
)

report_api_bp = Blueprint("report_api_bp", __name__)
reporter = PDFReporter()


@report_api_bp.post("/generate")
def generate_report():
    data = request.get_json() or {}
    rtype = data.get("type")  # grammar, automaton, regex
    title = data.get("title", "Reporte")

    try:
        dot = None
        info = {}

        if rtype == "grammar":
            g = parse_grammar(data.get("rules", []), data.get("start_symbol"))
            g = classify_grammar(g)

            viz = GrammarVisualizer()
            dot = viz.visualize(g)

            info = {
                "Tipo": g.metadata["classification"]["type"],
                "Variables": ", ".join(sorted(g.nonterminals)),
                "Terminales": ", ".join(sorted(g.terminals)),
            }

        elif rtype == "automaton":
            a = parse_automaton(data)
            a.metadata["type"] = data.get("detected_type", "Desconocido")

            try:
                viz = DFAVisualizer() if a.metadata["type"] == "AFD" else NFAVisualizer()
            except:
                viz = NFAVisualizer()

            dot = viz.visualize(a)

            info = {
                "Tipo": a.metadata["type"],
                "Estados": len(a.states),
                "Aceptación": ", ".join(sorted(a.accept)),
            }

        elif rtype == "regex":
            regex = data.get("regex", "")
            nfa = regex_to_nfa_epsilon(regex)
            dfa = nfa_epsilon_to_dfa(nfa)

            viz = DFAVisualizer()
            dot = viz.visualize(dfa)

            info = {
                "Expresión Regular": regex,
                "Estados AFD": len(dfa.states),
            }

        else:
            return jsonify({"success": False, "error": "Tipo inválido"}), 400

        path = reporter.generate_pdf(title, info, dot)

        return jsonify({
            "success": True,
            "file": os.path.relpath(path, "app")
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@report_api_bp.get("/list")
def list_reports():
    folder = "app/static/generated"
    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(".pdf")
    ]
    return jsonify({"success": True, "reports": files})
