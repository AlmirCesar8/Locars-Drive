from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo MarcaVeiculo
# -------------------------------------------------------

class MarcaVeiculo(db.Model):
    __tablename__ = 'Marca_Veiculo'

    id_Marca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Marca = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<MarcaVeiculo id={self.id_Marca} nome={self.Nome_Marca}>"