from flask import Blueprint
from app.models.usuario import Usuario
from app.models.cidade import Cidade

teste_bp = Blueprint('teste', __name__)

@teste_bp.route('/teste-db')
def teste_db():
    try:
        nome_cidade = []
        usuarios = Usuario.query.all()
        cidades = Cidade.query.all()
        for c in cidades:
            nome_cidade.append(c.Nome_Cidade)
        return f"Conexão OK! Número de usuários: {len(usuarios)}\nnomes das cidades: {', '.join(nome_cidade)}"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"