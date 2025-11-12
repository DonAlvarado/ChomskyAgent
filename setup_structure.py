# setup_structure.py
"""
Script automático para crear la estructura base del proyecto ChomskyAgent.
Ejecutar con:
    python setup_structure.py
"""

import os

# ===============================
# Árbol base del proyecto
# ===============================
PROJECT_STRUCTURE = {
    "app": {
        "Back": {
            "api": [
                "grammar_api.py",
                "automata_api.py",
                "converter_api.py",
                "report_api.py",
                "tutor_api.py",
                "agent_api.py",
            ],
            "front_cntrlls": [
                "home_routes.py",
                "dashboard_routes.py",
                "analyzer_routes.py",
                "tutor_routes.py",
                "chat_routes.py",
                "report_routes.py",
            ],
            "interfaces": [
                "IAnalyzer.py",
                "IVisualizer.py",
                "IGenerator.py",
                "IAgent.py",
            ],
            "classifier": [
                "grammar_parser.py",
                "automata_parser.py",
                "classifier_engine.py",
                "converter.py",
                "example_generator.py",
                "equivalence_checker.py",
                "explainable_ai.py",
                "visualizer.py",
                "pdf_reporter.py",
                "tutor_quiz.py",
            ],
            "utils": [
                "validators.py",
                "file_manager.py",
                "graph_utils.py",
                "logger.py",
                "config_loader.py",
            ],
            "files": ["models.py", "__init__.py"],
        },
        "AI": [
            "reasoner.py",
            "memory.py",
            "trainer.py",
            "chatbot.py",
            "action_manager.py",
            "nlp_utils.py",
            "llm_connector.py",
            "__init__.py",
        ],
        "Front": {
            "templates": [
                "intro.html",
                "layout.html",
                "dashboard.html",
                "analyzer.html",
                "tutor.html",
                "chat.html",
                "reports.html",
                "about.html",
            ],
            "static": {
                "css": ["main.css", "animations.css", "themes.css"],
                "js": ["app.js", "dashboard.js", "analyzer.js", "chat.js", "animations.js"],
                "icons": [],
                "images": [],
            },
            "resources": {
                "examples": [],
                "docs": [],
                "files": ["config.json"],
            },
        },
        "test": [
            "test_classifier.py",
            "test_visualizer.py",
            "test_agent.py",
            "test_routes.py",
            "test_api.py",
            "__init__.py",
        ],
        "files": ["app.py", "__init__.py"],
    },
    "files": [
        "run.py",
        "requirements.txt",
        "tailwind.config.js",
        "package.json",
        "README_ARCHITECTURE.md",
        ".gitignore",
    ],
}

# ===============================
# Funciones de creación
# ===============================
def create_file(path, content=""):
    """Crea un archivo con contenido opcional."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def create_structure(base_path, structure):
    """Crea recursivamente carpetas y archivos."""
    for name, content in structure.items():
        if name == "files":
            for file_name in content:
                file_path = os.path.join(base_path, file_name)
                create_file(file_path, f"# Placeholder for {file_name}\n")
        else:
            dir_path = os.path.join(base_path, name)
            os.makedirs(dir_path, exist_ok=True)
            if isinstance(content, dict):
                create_structure(dir_path, content)
            elif isinstance(content, list):
                for file_name in content:
                    path = os.path.join(dir_path, file_name)
                    create_file(path, f"# Placeholder for {file_name}\n")


# ===============================
# Ejecución principal
# ===============================
if __name__ == "__main__":
    BASE_DIR = os.path.join(os.getcwd(), "ChomskyAgent")
    os.makedirs(BASE_DIR, exist_ok=True)
    create_structure(BASE_DIR, PROJECT_STRUCTURE)
    print("✅ Estructura de proyecto ChomskyAgent creada con éxito.")
