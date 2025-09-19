from flask import Flask
from app.routes import blueprints

def create_app():
    app = Flask(__name__)
    # Configurações do app aqui (ex: SECRET_KEY, banco de dados, etc.)

    # Registrar todos os blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
