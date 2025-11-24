from app.extensions import db
from sqlalchemy import Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class AvaliacaoServico(db.Model):
    __tablename__ = 'avaliacao_servico'

    id_avaliacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Liga à locação avaliada
    fk_aluguel_id = db.Column(db.Integer, ForeignKey('aluguel.id_aluguel'), nullable=False)
    
    nota = db.Column(db.Integer, nullable=False) # Nota de 1 a 5
    comentarios = db.Column(db.Text, nullable=True)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Usado para avaliar o cliente (se foi pontual, causou danos, etc.)
    avaliacao_cliente = db.Column(db.Integer, nullable=True) # Nota de 1 a 5 para o comportamento do cliente

    # Relação
    aluguel = relationship('Aluguel', backref='avaliacoes')

    def __repr__(self):
        return f"<Avaliacao {self.id_avaliacao} - Nota: {self.nota}>"