from flask import Blueprint, request, jsonify
from Back.classifier.automata_parser import parse_automaton, detect_type
from Back.classifier.visualizer import DFAVisualizer, NFAVisualizer
from Back.classifier.converter import DFA
from graphviz import Source

from Back.utils.validators import is_valid_automaton
from Back.utils.logger import get_logger

automata_api_bp = Blueprint("automata_api_bp", __name__)
log = get_logger("AutomataAPI")


@automata_api_bp.post("/analyze")
def analyze_automata():
    data = request.get_json() or {}

    if not is_valid_automaton(data):
        log.error("Autómata inválido en /automata/analyze.")
        return jsonify({"success": False, "error": "Autómata inválido."}), 400

    try:
        a = parse_automaton(data)
        atype = detect_type(a)
        a.metadata["type"] = atype

        log.info(f"Autómata analizado. Tipo detectado: {atype}")

        return jsonify({
            "success": True,
            "automaton": a.to_dict(),
            "type": atype
        })
    except ValueError as e:
        log.error(f"Error de valor en /automata/analyze: {e}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        log.error(f"Error interno en /automata/analyze: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@automata_api_bp.post("/visualize")
def visualize_automata():
    data = request.get_json() or {}

    if not is_valid_automaton(data):
        log.error("Autómata inválido en /automata/visualize.")
        return jsonify({"success": False, "error": "Autómata inválido."}), 400

    try:
        a = parse_automaton(data)
        atype = detect_type(a)

        viz = DFAVisualizer() if atype == "AFD" else NFAVisualizer()

        # visualizer devuelve DOT → aquí lo convertimos a SVG
        dot = viz.visualize(a)
        svg = Source(dot).pipe(format="svg").decode("utf-8")

        log.info(f"Autómata visualizado como {atype}.")
        return jsonify({
            "success": True,
            "type": atype,
            "svg": svg
        })
    except ValueError as e:
        log.error(f"Error de valor en /automata/visualize: {e}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        log.error(f"Error interno en /automata/visualize: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@automata_api_bp.post("/visualize_min")
def visualize_min_dfa():
    data = request.get_json(force=True)
    afd = data.get("afd_min")
    if not afd:
        log.error("Falta AFD minimizado en /automata/visualize_min.")
        return {"success": False, "error": "Falta AFD minimizado."}, 400

    try:
        dfa_obj = DFA(
            states=set(afd["states"]),
            alphabet=set(afd["alphabet"]),
            start=afd["start"],
            accept=set(afd["accept"]),
            transitions=afd["transitions"]
        )

        viz = DFAVisualizer()
        dot = viz.visualize(dfa_obj)
        svg = Source(dot).pipe(format="svg").decode("utf-8")

        log.info("AFD minimizado visualizado correctamente.")
        return {"success": True, "svg": svg}
    except Exception as e:
        log.error(f"Error interno en /automata/visualize_min: {e}")
        return {"success": False, "error": str(e)}, 500
