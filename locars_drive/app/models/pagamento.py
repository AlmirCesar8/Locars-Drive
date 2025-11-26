# app/models/pagamento.py

from app.extensions import db
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship

# -------------------------------------------------------
# Modelo Pagamento (Tabela Pagamento_)
# -------------------------------------------------------
class Pagamento(db.Model):
    __tablename__ = 'Pagamento_'  

    id_Pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # NOVO CAMPO: FK para Aluguel (conforme DDL)
    fk_Aluguel_id_Aluguel = db.Column(db.Integer, ForeignKey('aluguel.id_aluguel'), nullable=False)
    
    Valor = db.Column(Numeric(10, 2), nullable=False)
    Data_Pagamento = db.Column(db.Date, nullable=False)
    Metodo = db.Column(db.String(50), nullable=False)
    
    # Usando db.Enum para mapear o tipo ENUM do MySQL
    Status_Pagamento = db.Column(db.Enum('Pago', 'Pendente', name='status_pagamento_enum'), nullable=False)

    # Relação
    aluguel = relationship('Aluguel', backref='pagamentos')

    def __repr__(self):
        return f"<Pagamento id={self.id_Pagamento} valor={self.Valor} status={self.Status_Pagamento}>"