from flask import Blueprint, request, jsonify
from Back.classifier.automata_parser import parse_automaton, detect_type
from Back.classifier.visualizer import DFAVisualizer, NFAVisualizer
from graphviz import Source

automata_api_bp = Blueprint("automata_api_bp", __name__)


@automata_api_bp.post("/analyze")
def analyze_automata():
    data = request.get_json() or {}

    try:
        a = parse_automaton(data)
        atype = detect_type(a)
        a.metadata["type"] = atype

        return jsonify({
            "success": True,
            "automaton": a.to_dict(),
            "type": atype
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@automata_api_bp.post("/visualize")
def visualize_automata():
    data = request.get_json() or {}

    try:
        a = parse_automaton(data)
        atype = detect_type(a)

        if atype == "AFD":
            viz = DFAVisualizer()
        else:
            viz = NFAVisualizer()

        dot = viz.visualize(a)
        svg = Source(dot).pipe(format="svg").decode("utf-8")

        return jsonify({
            "success": True,
            "type": atype,
            "svg": svg
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@automata_api_bp.post("/visualize_min")
def visualize_min_dfa():
    data = request.get_json(force=True)
    afd = data.get("afd_min")
    if not afd:
        return {"error": "Falta AFD minimizado."}, 400

    from Back.classifier.visualizer import DFAVisualizer
    vis = DFAVisualizer()

    svg = vis.visualize(afd)
    return {"success": True, "svg": svg}
