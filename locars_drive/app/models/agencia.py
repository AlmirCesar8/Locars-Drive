from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Agencia
# -------------------------------------------------------

class Agencia(db.Model):
    __tablename__ = 'Agencia'
    
    id_Agencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Agencia = db.Column(db.String(255), nullable=False)
    Num_Agencia = db.Column(db.Integer, nullable=False, unique=True)
    
    ### Rever relacionamento com cidades
    
    def __repr__(self):
        return f"<Agencia id={self.id_Agencia} nome={self.Nome_Agencia} num={self.Num_Agencia}>"