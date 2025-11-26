# app/models/funcao.py

from app.extensions import db 
from sqlalchemy import Numeric, Date, String

# -------------------------------------------------------
# Modelo de Função
# -------------------------------------------------------

class Funcao(db.Model):
    __tablename__ = 'Funcao'

    id_Funcao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Funcao = db.Column(db.String(255), nullable=False, unique=True)
    Descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Funcao id={self.id_Funcao} nome={self.Nome_Funcao} descricao={self.Descricao}>"