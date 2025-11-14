from __future__ import annotations
import uuid
import random
from typing import Dict, Any

from Back.classifier.example_generator import generate
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.utils.logger import get_logger

log = get_logger("TutorQuiz")


class TutorQuiz:

    # SELECCIÓN DE TIPOS: pesos
    TYPE_WEIGHTS = {
        "regular": 0.30,     # Tipo 3
        "cfl": 0.30,         # Tipo 2
        "context": 0.20,     # Tipo 1
        "irrestrict": 0.20   # Tipo 0
    }

    # 1. GENERACIÓN DE PREGUNTAS
    def make_question(self, difficulty: str = "basic") -> Dict[str, Any]:

        # Selección ponderada según los pesos
        types = list(self.TYPE_WEIGHTS.keys())
        weights = list(self.TYPE_WEIGHTS.values())

        chosen = random.choices(types, weights)[0]

        example = generate(chosen)

        log.info(f"Pregunta generada tipo={example['type']} ({chosen}).")

        return {
            "id": str(uuid.uuid4()),
            "type": "classify_grammar",
            "question": example["productions"]
        }

    # 2. CORRECCIÓN DE RESPUESTA
    def check_answer(self, qtype: str, question: Dict[str, Any], answer: str) -> Dict[str, Any]:

        if qtype != "classify_grammar":
            return {"error": "tipo inválido"}

        # Construir gramática
        prods = [f"{A} -> " + " | ".join(rhs) for A, rhs in question.items()]
        grammar = parse_grammar(prods)
        classified = classify_grammar(grammar)

        correct_full = classified.metadata["classification"]["type"]
        correct_simple = correct_full.split("(")[0].strip() 
        user_simple = answer.strip()

        correct = (user_simple.lower() == correct_simple.lower())

        log.info(
            f"Tutor: usuario='{answer}', correcto='{correct_simple}', real='{correct_full}', result={correct}"
        )

        return {
            "correct": correct,
            "correct_type": correct_full
        }
