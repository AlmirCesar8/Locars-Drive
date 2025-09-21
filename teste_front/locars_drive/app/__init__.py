from flask import Flask

# Importar todos os blueprints
from app.routes.index import index_bp
from app.routes.contato import contato_bp
from app.routes.frotas import frotas_bp
from app.routes.locacao import locacao_bp
from app.routes.planos import planos_bp
from app.routes.veiculos import veiculos_bp
from app.routes.administrador import administrador_bp
from app.routes.autenticacao import autenticacao_bp
from app.routes.devolucao import devolucao_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

    # Registrar blueprints
    app.register_blueprint(index_bp)  # Rota principal '/'
    app.register_blueprint(contato_bp, url_prefix='/contato')
    app.register_blueprint(frotas_bp, url_prefix='/frotas')
    app.register_blueprint(locacao_bp, url_prefix='/locacao')
    app.register_blueprint(planos_bp, url_prefix='/planos')
    app.register_blueprint(veiculos_bp, url_prefix='/veiculos')
    app.register_blueprint(administrador_bp, url_prefix='/admin')
    app.register_blueprint(autenticacao_bp, url_prefix='/auth')
    app.register_blueprint(devolucao_bp, url_prefix='/devolucao')

    return app
