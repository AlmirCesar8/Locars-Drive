# app/models/agencia.py

from app.extensions import db
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship # Import necessário para relacionamentos

# -------------------------------------------------------
# Modelo de Agencia
# -------------------------------------------------------

class Agencia(db.Model):
    __tablename__ = 'Agencia'
    
    id_Agencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Agencia = db.Column(db.String(255), nullable=False)
    Num_Agencia = db.Column(db.Integer, nullable=False, unique=True)
    fk_Endereco_id = db.Column(db.Integer, db.ForeignKey('Endereco.id_Endereco'), nullable=False)
    
    # Relação: Permite acessar os detalhes do endereço
    endereco = relationship('Endereco', backref='agencias')
    
    def __repr__(self):
        return f"<Agencia id={self.id_Agencia} nome={self.Nome_Agencia} num={self.Num_Agencia}>"