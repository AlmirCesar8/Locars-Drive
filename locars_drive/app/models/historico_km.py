from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Historico_KM
# -------------------------------------------------------
class Historico_KM(db.Model):
    __tablename__ = 'historico_km'  # Nome da tabela no banco de dados

    id_km = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id_Veiculo = db.Column(db.Integer, db.ForeignKey('Veiculo.id_Veiculo'), nullable=False)
    Data_Registro = db.Column(db.Date, nullable=False)
    # CORRIGIDO: Usando 'Numeric' que é o tipo de dado importado do sqlalchemy
    Km_Registrado = db.Column(Numeric(10, 2), nullable=False)

    # veiculo = db.relationship('Veiculo', back_populates='historicos_km')

    def __repr__(self):
        return f"<Historico_KM id={self.id_km} data={self.Data_Registro} km={self.Km_Registrado}>"