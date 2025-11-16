from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo Veículo
# -------------------------------------------------------

class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id_Veiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Frota = db.Column(db.Integer, nullable=False)
    Placa = db.Column(db.String(7), unique=True, nullable=False)
    Km_Rodado = db.Column(db.Numeric(10,2), nullable=False)
    StatusVeiculo = db.Column(db.Enum('Disponível', 'Indisponível'), nullable=False)

    def __repr__(self):
        return f"<Veiculo id={self.id_Veiculo} placa={self.Placa} frota={self.Frota} status={self.StatusVeiculo}>"