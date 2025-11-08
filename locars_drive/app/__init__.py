from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialização das extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Configurações do Login Manager
    login_manager.login_view = 'autenticacao.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'info'  # para exibir o flash de forma estilizada

    # Carregamento do usuário logado
    @login_manager.user_loader
    def load_user(user_id):
        from app.modelos import Usuario
        return Usuario.query.get(int(user_id))

    # Registrar todos os Blueprints
    from app.routes import blueprints
    for bp, prefix in blueprints:
        if prefix:
            app.register_blueprint(bp, url_prefix=prefix)
        else:
            app.register_blueprint(bp)

    # Criar tabelas automaticamente (opcional, útil durante o desenvolvimento)
    with app.app_context():
        db.create_all()

    return app
