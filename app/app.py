from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(
        __name__,
        template_folder="Front/templates",
        static_folder="Front/static",
    )

    # Config básica
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSON_AS_ASCII"] = False
    app.config["SECRET_KEY"] = "chomsky-agent-dev-key"

    # Habilitar CORS
    CORS(app)

    # ============================
    # BLUEPRINTS DE VISTAS (HTML)
    # ============================
    from Back.front_cntrlls.home_routes import home_bp
    from Back.front_cntrlls.dashboard_routes import dashboard_bp
    from Back.front_cntrlls.analyzer_routes import analyzer_bp
    from Back.front_cntrlls.tutor_routes import tutor_bp
    from Back.front_cntrlls.chat_routes import chat_bp
    from Back.front_cntrlls.report_routes import report_pages_bp
    from Back.front_cntrlls.converter_routes import converter_routes_bp
    from Back.front_cntrlls.compare_routes import compare_routes_bp

    # NUEVO: Página Acerca de
    from Back.front_cntrlls.about_routes import about_bp

    # Registro de blueprints del Frontend
    app.register_blueprint(home_bp)                  # /
    app.register_blueprint(dashboard_bp)             # /dashboard
    app.register_blueprint(analyzer_bp)              # /analyzer
    app.register_blueprint(tutor_bp)                 # /tutor
    app.register_blueprint(chat_bp)                  # /chat
    app.register_blueprint(report_pages_bp)          # /reports
    app.register_blueprint(converter_routes_bp)      # /converter
    app.register_blueprint(compare_routes_bp)        # /compare
    app.register_blueprint(about_bp)                 # /about

    # ============================
    # BLUEPRINTS API (JSON)
    # ============================
    from Back.api.grammar_api import grammar_api_bp
    from Back.api.automata_api import automata_api_bp
    from Back.api.converter_api import converter_api_bp
    from Back.api.report_api import report_api_bp
    from Back.api.tutor_api import tutor_api_bp
    from Back.api.agent_api import agent_api_bp
    from Back.api.compare_api import compare_api_bp

    app.register_blueprint(grammar_api_bp, url_prefix="/api/grammar")
    app.register_blueprint(automata_api_bp, url_prefix="/api/automata")
    app.register_blueprint(converter_api_bp, url_prefix="/api/converter")
    app.register_blueprint(report_api_bp, url_prefix="/api/report")
    app.register_blueprint(tutor_api_bp, url_prefix="/api/tutor")
    app.register_blueprint(agent_api_bp, url_prefix="/api/agent")
    app.register_blueprint(compare_api_bp, url_prefix="/api/compare")

    # ============================
    # HEALTHCHECK
    # ============================
    @app.get("/ping")
    def ping():
        return {"status": "ok", "app": "ChomskyAgent"}

    return app


# Punto de entrada directo
if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
