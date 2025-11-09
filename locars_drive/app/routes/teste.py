from flask import Blueprint
from app.modelos import Usuario

teste_bp = Blueprint('teste', __name__)

@teste_bp.route('/teste-db')
def teste_db():
    try:
        usuarios = Usuario.query.all()
        return f"Conexão OK! Número de usuários: {len(usuarios)}"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"