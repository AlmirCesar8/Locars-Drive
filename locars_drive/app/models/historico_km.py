# app/models/historico_km.py

from app.extensions import db
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship

# -------------------------------------------------------
# Modelo de Historico_KM
# -------------------------------------------------------
class Historico_KM(db.Model):
    __tablename__ = 'historico_km'

    id_km = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # NOVO CAMPO: FK para Veiculo
    fk_Veiculo_id_Veiculo = db.Column(db.Integer, db.ForeignKey('veiculo.id_Veiculo'), nullable=False)
    
    Data_Registro = db.Column(db.Date, nullable=False)
    Km_Registrado = db.Column(Numeric(10, 2), nullable=False)

    # Relação: Permite acessar o veículo
    veiculo = relationship('Veiculo', backref='historicos_km')

    def __repr__(self):
        return f"<Historico_KM id={self.id_km} data={self.Data_Registro} km={self.Km_Registrado}>"