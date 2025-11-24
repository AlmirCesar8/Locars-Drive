from app.extensions import db
from sqlalchemy import Numeric, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Vistoria(db.Model):
    __tablename__ = 'vistoria'

    id_vistoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Liga ao Aluguel
    fk_aluguel_id = db.Column(db.Integer, ForeignKey('aluguel.id_aluguel'), nullable=False)
    
    tipo = db.Column(db.String(10), nullable=False) # 'Check-out' ou 'Check-in'
    
    # Dados coletados
    nivel_combustivel = db.Column(db.Numeric(3, 2), nullable=False) # 0.00 a 1.00 (ou seja, 0% a 100%)
    quilometragem = db.Column(db.Integer, nullable=False)
    avarias_json = db.Column(db.Text, nullable=True) # JSON ou string para registrar danos
    
    data_vistoria = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relação
    aluguel = relationship('Aluguel', backref='vistorias')

    def __repr__(self):
        return f"<Vistoria {self.id_vistoria} - Tipo: {self.tipo} - Aluguel: {self.fk_aluguel_id}>"