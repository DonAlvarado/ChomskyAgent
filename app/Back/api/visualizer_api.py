from flask import Blueprint, request, jsonify
from Back.classifier.visualizer import visualize_dfa

viz_api_bp = Blueprint("viz_api_bp", __name__)

@viz_api_bp.post("/dfa")
def viz_dfa():
    # recibir DFA ya parseado
    ...
    #dot = visualize_dfa(dfa)
    #return jsonify({"dot": dot})
