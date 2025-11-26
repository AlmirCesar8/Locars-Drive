# app/models/modelo.py

from app.extensions import db
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship 
# Seus imports podem variar, garanta que ForeignKey e relationship estejam importados

# -------------------------------------------------------
# Modelo Modelo 
# -------------------------------------------------------
class Modelo(db.Model):
    __tablename__ = 'Modelo'

    id_Modelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Modelo = db.Column(db.String(255), nullable=False, unique=True)


    def __repr__(self):
        return f"<Modelo id={self.id_Modelo} nome={self.Nome_Modelo}>"