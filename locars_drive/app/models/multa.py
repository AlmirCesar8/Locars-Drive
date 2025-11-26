# app/models/multa.py

from app.extensions import db
from sqlalchemy import Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

# -------------------------------------------------------
# Modelo Multa (Tabela Multa)
# -------------------------------------------------------
class Multa(db.Model):
    __tablename__ = 'Multa'

    id_Multa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_Aluguel_id_Aluguel = db.Column(db.Integer, ForeignKey('aluguel.id_aluguel'), nullable=False)

    Motivo_Multa = db.Column(db.Text, nullable=False)
    Valor = db.Column(Numeric(10, 2), nullable=False) 
    Data_Multa = db.Column(db.DateTime, nullable=False)

    # Relação
    aluguel = relationship('Aluguel', backref='multas')

    def __repr__(self):
        return f"<Multa id={self.id_Multa} valor={self.Valor} data={self.Data_Multa}>"