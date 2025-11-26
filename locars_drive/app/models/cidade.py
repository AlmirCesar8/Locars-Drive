# app/models/cidade.py

from app.extensions import db 
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship # Import necessário para relacionamentos

# -------------------------------------------------------
# Modelo de Cidade (AGORA APENAS DADOS GEOGRÁFICOS)
# -------------------------------------------------------
class Cidade(db.Model):
    __tablename__ = 'Cidade'  

    id_Cidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Cidade = db.Column(db.String(255), nullable=False, unique=True)
    
    # NOVO CAMPO: FK para Estado
    fk_Estado_id_Estado = db.Column(db.Integer, db.ForeignKey('Estado.id_Estado'), nullable=False)
    
    # Relações
    # Permite acessar o estado a partir da cidade
    estado = relationship('Estado', backref='cidades')

    def __repr__(self):
        # Acesso direto ao Nome_Cidade e ao estado (via relationship)
        return f"<Cidade id={self.id_Cidade} nome={self.Nome_Cidade} estado={self.estado.Nome_Estado}>"