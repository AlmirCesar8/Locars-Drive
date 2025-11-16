from app.extensions import db  # usa a extensão global configurada no __init__.py
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Função
# -------------------------------------------------------

class Funcao(db.Model):
    __tablename__ = 'Funcao'

    id_Funcao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Funcao_ = db.Column(db.String(255), nullable=False, unique=True)
    Descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Funcao id={self.id_Funcao} nome={self.Nome_Funcao_} descricao={self.Descricao}>"