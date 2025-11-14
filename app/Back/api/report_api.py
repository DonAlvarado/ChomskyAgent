from flask import Blueprint, request, jsonify
import os

from Back.classifier.pdf_reporter import PDFReporter
from Back.classifier.visualizer import GrammarVisualizer, DFAVisualizer, NFAVisualizer
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.classifier.automata_parser import parse_automaton
from Back.classifier.converter import regex_to_nfa_epsilon, nfa_epsilon_to_dfa

from Back.utils.validators import (
    is_valid_grammar,
    is_valid_automaton,
    is_valid_regex
)
from Back.utils.logger import get_logger

report_api_bp = Blueprint("report_api_bp", __name__)
reporter = PDFReporter()
log = get_logger("ReportAPI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.normpath(os.path.join(
    BASE_DIR, "..", "..", "Front", "static", "generated"
))


@report_api_bp.post("/generate")
def generate_report():
    data = request.get_json() or {}
    rtype = data.get("type")
    title = data.get("title", "Reporte")

    path = None
    info = {}

    try:
        if rtype == "grammar":
            rules = data.get("rules", [])
            start_symbol = data.get("start_symbol")

            if not is_valid_grammar(rules):
                return jsonify({"success": False, "error": "Gramática inválida"}), 400

            g = classify_grammar(parse_grammar(rules, start_symbol))
            dot = GrammarVisualizer().visualize(g)

            info = {
                "Tipo": g.metadata["classification"]["type"],
                "Variables": ", ".join(sorted(g.nonterminals)),
                "Terminales": ", ".join(sorted(g.terminals)),
            }

        elif rtype == "automaton":
            automaton = data.get("automaton", {})
            if not is_valid_automaton(automaton):
                return jsonify({"success": False, "error": "Autómata inválido"}), 400

            a = parse_automaton(automaton)
            atype = automaton.get("detected_type", "Desconocido")

            viz = DFAVisualizer() if atype == "AFD" else NFAVisualizer()
            dot = viz.visualize(a)

            info = {
                "Tipo": atype,
                "Estados": len(a.states),
                "Aceptación": ", ".join(sorted(a.accept)),
            }

        elif rtype == "regex":
            regex = data.get("regex", "")
            if not is_valid_regex(regex):
                return jsonify({"success": False, "error": "Regex inválida"}), 400

            nfa = regex_to_nfa_epsilon(regex)
            dfa = nfa_epsilon_to_dfa(nfa)

            dot = DFAVisualizer().visualize(dfa)

            info = {
                "Expresión Regular": regex,
                "Estados AFD": len(dfa.states),
            }

        else:
            return jsonify({"success": False, "error": "Tipo inválido"}), 400

        path = reporter.generate_pdf(title, info, dot)

        # Solo el nombre del archivo, no la ruta completa
        file_name = os.path.basename(path)

        return jsonify({"success": True, "file": file_name})

    except Exception as e:
        log.error(f"Error generando PDF: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@report_api_bp.get("/list")
def list_reports():
    try:
        dir_path = GENERATED_DIR

        if not os.path.exists(dir_path):
            return jsonify({"success": True, "files": []})

        files = [
            f for f in os.listdir(dir_path)
            if f.lower().endswith(".pdf")
        ]

        return jsonify({
            "success": True,
            "files": files
        })

    except Exception as e:
        log.error(f"Error listando reportes: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
