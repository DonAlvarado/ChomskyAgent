from __future__ import annotations
import uuid
from typing import Dict, Any

from Back.classifier.example_generator import generate
from Back.classifier.grammar_parser import parse_grammar
from Back.classifier.classifier_engine import classify_grammar
from Back.utils.logger import get_logger

log = get_logger("TutorQuiz")


class TutorQuiz:
    def make_question(self, difficulty: str = "basic") -> Dict[str, Any]:
        if difficulty == "basic":
            example = generate("regular")
            log.info("Pregunta generada (regular).")
            return {
                "id": str(uuid.uuid4()),
                "type": "classify_grammar",
                "question": example["productions"]
            }

        if difficulty == "cfl":
            example = generate("cfl")
            log.info("Pregunta generada (CFL).")
            return {
                "id": str(uuid.uuid4()),
                "type": "classify_grammar",
                "question": example["productions"]
            }

        log.error(f"Dificultad inválida: {difficulty}")
        return {"error": "dificultad inválida"}

    def check_answer(self, qtype: str, question: Dict[str, Any], answer: str) -> Dict[str, Any]:
        if qtype != "classify_grammar":
            log.error(f"Tipo de pregunta inválido: {qtype}")
            return {"error": "tipo inválido"}

        prods = [f"{A} -> " + " | ".join(rhs) for A, rhs in question.items()]
        grammar = parse_grammar(prods)
        classified = classify_grammar(grammar)
        correct_type = classified.metadata["classification"]["type"]

        correct = (answer.strip().lower() == correct_type.lower())

        log.info(f"Respuesta evaluada. Usuario: {answer}, Correcta: {correct_type}, Resultado: {correct}")

        return {
            "correct": correct,
            "correct_type": correct_type,
        }
