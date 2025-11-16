from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo País
# -------------------------------------------------------

class Pais(db.Model):
    __tablename__ = 'Pais'

    id_Pais = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Pais = db.Column(db.String(255), nullable=False, unique=True)
    Sigla_ = db.Column(db.String(3), nullable=False, unique=True)

    def __repr__(self):
        return f"<Pais id={self.id_Pais} nome={self.Nome_Pais} sigla={self.Sigla}>"
