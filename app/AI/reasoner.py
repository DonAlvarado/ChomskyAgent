# reasoner.py
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Intent:
    action: str
    extra: Dict[str, Any] | None = None


class Reasoner:

    # ===============================
    # DETECCIÓN DE INTENCIÓN
    # ===============================
    def infer_intent(self, msg: str) -> Intent:
        m = msg.lower()

        # 1. Explicación de gramática (prioridad sobre análisis)
        if "explica" in m:
            return Intent(action="EXPLAIN_GRAMMAR")

        # 2. Gramáticas: cualquier cosa con ->
        if "->" in m or "→" in m:
            return Intent(action="ANALYZE_GRAMMAR")

        # 3. Autómatas
        if "autómata" in m or "automata" in m or "afd" in m or "afn" in m:
            return Intent(action="ANALYZE_AUTOMATON")

        # 4. Regex
        if "regex" in m or "expresión regular" in m or "expresion regular" in m:
            return Intent(action="CONVERT_REPRESENTATION")

        # 5. Tutor
        if "pregunta" in m or "tutor" in m or "quiz" in m:
            return Intent(action="TUTOR_QUESTION")

        if "respuesta" in m or "respondo" in m:
            return Intent(action="TUTOR_CHECK")

        # 6. PDF
        if "pdf" in m or "reporte" in m:
            return Intent(action="GENERATE_PDF")

        # fallback
        return Intent(action="UNKNOWN")

    # ===============================
    # FORMATEADOR
    # ===============================
    def format_reply(self, intent: Intent, raw: Dict[str, Any]) -> str:
        if raw is None:
            return "<span class='text-red-600 font-semibold'>Hubo un problema inesperado.</span>"

        if not raw.get("success", True):
            return f"<span class='text-red-600 font-semibold'>Error:</span> {raw.get('error')}"

        # -------- GRAMÁTICA --------
        if intent.action == "ANALYZE_GRAMMAR":
            cls = raw.get("classification", {})
            gtype = cls.get("type", "Desconocido")
            steps = cls.get("steps", [])

            html = f"""
            <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
                <div class="text-lg font-bold text-indigo-700 mb-2">
                    🧩 Clasificación de la Gramática
                </div>

                <div class="text-gray-800 mb-3">
                    <b>Tipo detectado:</b>
                    <span class="text-indigo-600 font-semibold">{gtype}</span>
                </div>

                <div class="font-semibold mb-1 text-gray-700">Razones:</div>
                <ul class="list-disc pl-6 text-gray-800">
            """
            for s in steps:
                html += f"<li>{s}</li>"

            html += "</ul></div>"
            return html

        # -------- EXPLICACIÓN --------
        if intent.action == "EXPLAIN_GRAMMAR":
            text = raw.get("explanation", "No tengo detalles adicionales.")
            return f"""
            <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
                <b class="text-indigo-700">Explicación:</b>
                <div class="mt-2 text-gray-800">{text}</div>
            </div>
            """

        # -------- AUTÓMATA --------
        if intent.action == "ANALYZE_AUTOMATON":
            t = raw.get("type", "Desconocido")
            auto = raw.get("automaton", {})
            states = auto.get("states", [])
            alphabet = auto.get("alphabet", [])

            return f"""
            <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
                <div class="text-lg font-bold text-blue-700 mb-2">
                    🔷 Clasificación del Autómata
                </div>
                <div class="text-gray-800">
                    <b>Tipo detectado:</b> <span class="text-blue-600">{t}</span><br/>
                    <b>Estados:</b> {len(states)}<br/>
                    <b>Alfabeto:</b> {{{", ".join(alphabet)}}}
                </div>
            </div>
            """

        # -------- REGEX --------
        if intent.action == "CONVERT_REPRESENTATION":
            afd = raw.get("afd")
            if afd:
                num_states = len(afd.get("states", []))
                alphabet = afd.get("alphabet", [])
                return f"""
                <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
                    <div class="text-lg font-bold text-purple-700 mb-2">
                        🔤 Conversión de Expresión Regular
                    </div>
                    <div class="text-gray-800">
                        Se generó un AFD con <b>{num_states}</b> estados.<br/>
                        <b>Alfabeto:</b> {{{", ".join(alphabet)}}}
                    </div>
                </div>
                """
            return """
            <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
                No pude generar el AFD a partir de la expresión regular.
            </div>
            """

        # -------- PDF --------
        if intent.action == "GENERATE_PDF":
            file = raw.get("file", None)
            if not file:
                return "Error al generar PDF."

            return f"""
            <div class="p-3 rounded-xl bg-green-100 border border-green-300 shadow-sm">
                📄 <b class="text-green-700">PDF generado correctamente:</b>
                <a href="/static/generated/{file}" class="text-green-800 underline" target="_blank">
                    Descargar PDF
                </a>
            </div>
            """

        # -------- TUTOR (Pregunta) --------
        if intent.action == "TUTOR_QUESTION":
            q = raw.get("question", "No hay preguntas disponibles.")
            return f"""
            <div class="p-3 rounded-xl bg-yellow-100 border border-yellow-300 shadow-sm">
                🧠 <b class="text-yellow-700">Pregunta del Tutor:</b>
                <div class="mt-2 text-gray-800">{q}</div>
            </div>
            """

        # -------- TUTOR (Respuesta) --------
        if intent.action == "TUTOR_CHECK":
            res = raw.get("result", "Respuesta procesada.")
            return f"<div class='p-3 bg-gray-100 border rounded'>{res}</div>"

        return """
        <div class="p-3 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
            🤖 No entendí qué querés hacer, pero puedo ayudarte a analizar 
            <b>gramáticas</b>, <b>autómatas</b> o <b>expresiones regulares</b>.
        </div>
        """
