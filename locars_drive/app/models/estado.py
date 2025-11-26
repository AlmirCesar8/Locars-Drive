# app/models/estado.py

from app.extensions import db 
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship # Import necessário para relacionamentos

# -------------------------------------------------------
# Modelo de Estado
# -------------------------------------------------------

class Estado(db.Model):
    __tablename__ = 'Estado' 

    id_Estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Estado = db.Column(db.String(255), nullable=False, unique=True)
    Regiao = db.Column(db.String(255), nullable=False)
    
    # NOVO CAMPO: FK para Pais
    fk_Pais_id_Pais = db.Column(db.Integer, db.ForeignKey('Pais.id_Pais'), nullable=False)

    # Relação: Permite acessar o país
    pais = relationship('Pais', backref='estados')
    
    # Relação: As cidades estão acessíveis através do backref 'cidades' em Cidade
    
    def __repr__(self):
        return f"<Estado id={self.id_Estado} nome={self.Nome_Estado} regiao={self.Regiao}>"