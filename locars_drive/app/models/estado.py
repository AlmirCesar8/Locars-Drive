from app.extensions import db 
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Estado
# -------------------------------------------------------

class Estado(db.Model):
    __tablename__ = 'Estado' 

    id_Estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Estado = db.Column(db.String(255), nullable=False, unique=True)
    Regiao = db.Column(db.String(255), nullable=False)

### sera que precisa desse tamanho todo pra sigla e para nome???

    def __repr__(self):
        return f"<Estado id={self.id_Estado} nome={self.Nome_Estado} regiao={self.Regiao}>"