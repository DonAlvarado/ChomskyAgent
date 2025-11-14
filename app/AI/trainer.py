import json
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline


# 1. Dataset de entrenamiento

TRAINING_DATA = [
    # ANALYZE
    ("analiza esta gramática", "analyze"),
    ("puedes analizar esto", "analyze"),
    ("quiero saber de qué tipo es", "analyze"),
    ("clasifica esta gramática", "analyze"),

    # EXPLAIN
    ("explica por qué es ese tipo", "explain"),
    ("muéstrame la explicación", "explain"),
    ("cómo llegaste a ese resultado", "explain"),
    ("explícame la clasificación", "explain"),

    # CONVERTER
    ("convierte esta regex", "convert"),
    ("quiero el AFD de esta regex", "convert"),
    ("pásalo a gramática regular", "convert"),
    ("haz la conversión", "convert"),

    # EXAMPLES
    ("dame un ejemplo de tipo 2", "example"),
    ("genera una gramática tipo 3", "example"),
    ("necesito un ejemplo automático", "example"),
    ("crea un ejemplo aleatorio", "example"),

    # PDF
    ("haz un pdf", "pdf"),
    ("genera el reporte", "pdf"),
    ("quiero descargar el reporte", "pdf"),
    ("crea el informe en pdf", "pdf"),

    # TUTOR
    ("quiero practicar", "tutor"),
    ("dame un ejercicio", "tutor"),
    ("modo quiz", "tutor"),
    ("vamos a practicar", "tutor"),

    # COMPARISON
    ("compara estas gramáticas", "compare"),
    ("quiero saber si estas dos gramáticas son iguales", "compare"),
    ("verifica equivalencia", "compare"),
    ("son equivalentes estos lenguajes", "compare"),

    # CHAT SMALLTALK
    ("hola", "smalltalk"),
    ("qué tal", "smalltalk"),
    ("cómo estás", "smalltalk"),
    ("saludos", "smalltalk"),
]



# 2. Entrenamiento
def train_intent_model(output_path="intent_model.pkl"):
    """
    Entrena un modelo TF-IDF + LinearSVC basado en TRAINING_DATA.
    Guarda el modelo en un archivo .pkl.
    """

    texts = [t[0] for t in TRAINING_DATA]
    labels = [t[1] for t in TRAINING_DATA]

    # Pipeline: vectorizador + clasificador
    clf = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("svc", LinearSVC())
    ])

    print("[Trainer] Entrenando modelo...")
    clf.fit(texts, labels)
    print("[Trainer] Entrenamiento completado.")

    # Guardar modelo
    joblib.dump(clf, output_path)
    print(f"[Trainer] Modelo guardado en: {output_path}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "intent_model.pkl")

    train_intent_model(MODEL_PATH)
