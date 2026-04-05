from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates")

    from app.routes import main
    app.register_blueprint(main)

    return app