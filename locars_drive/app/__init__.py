from flask import Flask
from .config import Config
from app.extensions import db, bcrypt, login_manager


def create_app():
    app = Flask(__name__)
    
    # Carrega corretamente a classe de configuração
    app.config.from_object(Config)

    # Inicializar extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Configurações do login
    login_manager.login_view = 'autenticacao.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.routes import blueprints
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix or None)

    print("Aplicativo criado com sucesso!")

    return app
