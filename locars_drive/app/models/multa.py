from app.extensions import db
# Importe os tipos corretos do SQLAlchemy
from sqlalchemy import Numeric, DateTime, Text

# -------------------------------------------------------
# Modelo Multa (Tabela Multa)
# -------------------------------------------------------
class Multa(db.Model):
    __tablename__ = 'Multa'  # Nome da tabela no banco de dados

    # Colunas conforme o DDL
    id_Multa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Text é equivalente a db.Text ou db.String longo
    Motivo_Multa = db.Column(db.Text, nullable=False)
    
    # CORREÇÃO: Usando Numeric no lugar de db.Decimal
    # Se precisar de precisão, use Numeric(10, 2), mas Numeric simples também funciona.
    Valor = db.Column(Numeric, nullable=False) 
    
    Data_Multa = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Multa id={self.id_Multa} valor={self.Valor} data={self.Data_Multa}>"