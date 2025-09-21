from app.routes.index import index_bp
from app.routes.erros import erros_bp
from app.routes.frotas import frotas_bp
from app.routes.locacao import locacao_bp
from app.routes.planos import planos_bp
from app.routes.veiculos import veiculos_bp
from app.routes.contato import contato_bp
from app.routes.autenticacao import autenticacao_bp
from app.routes.administrador import administrador_bp
from app.routes.devolucao import devolucao_bp

blueprints = [
    index_bp,
    erros_bp,
    frotas_bp,
    locacao_bp,
    planos_bp,
    veiculos_bp,
    contato_bp,
    autenticacao_bp,
    administrador_bp,
    devolucao_bp,
]