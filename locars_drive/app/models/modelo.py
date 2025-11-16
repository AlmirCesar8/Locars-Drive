from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo Modelo 
# -------------------------------------------------------

class Modelo(db.Model):
    __tablename__ = 'Modelo'

    id_Modelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Modelo = db.Column(db.String(255), nullable=False, unique=True)
    # fabricante = db.Column(db.String(100), nullable=False)
    # ano = db.Column(db.Integer, nullable=False)
    # categoria = db.Column(db.String(50), nullable=False)

# sera quw não precisa de mais campos e dessas conecções?

    def __repr__(self):
        return f"<Modelo id={self.id_Modelo} nome={self.Nome_Modelo}>"