# app/models/funcao.py

from app.extensions import db 
from sqlalchemy import Numeric, Date, String

# -------------------------------------------------------
# Modelo de Função
# -------------------------------------------------------

class Funcao(db.Model):
    __tablename__ = 'funcao'

    id_funcao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_funcao = db.Column(db.String(255), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Funcao id={self.id_Funcao} nome={self.Nome_Funcao} descricao={self.Descricao}>"