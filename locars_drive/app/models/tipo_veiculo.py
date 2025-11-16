from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo Tipo-Veículo
# -------------------------------------------------------

class TipoVeiculo(db.Model):
    __tablename__ = 'Tipo_Veiculo'

    id_Tipo = db.Column(db.Integer, primary_key=True)
    Nome_Tipo = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return f"<TipoVeiculo id={self.id_Tipo} nome={self.Nome_Tipo}>"
