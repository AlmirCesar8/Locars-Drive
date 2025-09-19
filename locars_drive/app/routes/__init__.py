from flask import Blueprint

# Importar blueprints dos módulos
from app.routes.index import index_bp
from app.routes.autenticacao import autenticacao_bp
from app.routes.administrador import administrador_bp
# importe outros blueprints conforme necessário

# Opcionalmente, criar um registro centralizado dos blueprints
blueprints = [
    index_bp,
    autenticacao_bp,
    administrador_bp,
    # outros blueprints
]
