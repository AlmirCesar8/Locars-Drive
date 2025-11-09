from flask import Flask
from app.extensions import db, bcrypt, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

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

    print("Aplicativo criado com sucesso!")
    return app


