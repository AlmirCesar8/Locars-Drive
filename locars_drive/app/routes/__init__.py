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
        (index_bp, None),  # Rota principal '/'
        (contato_bp, '/contato'),
        (frotas_bp, '/frotas'),
        (locacao_bp, '/locacao'),
        (planos_bp, '/planos'),
        (veiculos_bp, '/veiculos'),
        (administrador_bp, '/admin'),
        (autenticacao_bp, '/auth'),
        (devolucao_bp, '/devolucao'),
    ]