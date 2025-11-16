from app.extensions import db 
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Cidade
# -------------------------------------------------------
class Cidade(db.Model):
    __tablename__ = 'Cidade'  # Nome da tabela no banco de dados

    id_Cidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Cidade = db.Column(db.String(255), nullable=False, unique=True)
    CEP_ = db.Column(db.String(8), nullable=False, unique=True)
    Complemento = db.Column(db.String(50), nullable=True)
    Bairro = db.Column(db.String(255), nullable=False)
    Num_Casa = db.Column(db.Integer, nullable=False, unique=True)
    
    ### será q num-casa deve ser unico?
    
    def __repr__(self):
        return f"<Cidade id={self.id_Cidade} nome={self.Nome_Cidade} bairro={self.Bairro} cep={self.CEP_}>"