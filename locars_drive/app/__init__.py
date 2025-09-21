from flask import Flask
from app.routes import blueprints
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'claudete_eu_te_amo'

    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app
