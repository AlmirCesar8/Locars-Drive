from app.extensions import db
from sqlalchemy import Numeric, Date, String

# -------------------------------------------------------
# Modelo Pagamento (Tabela Pagamento_)
# -------------------------------------------------------
class Pagamento(db.Model):
    # CORREÇÃO: Nome da tabela é Pagamento_ (com underscore)
    __tablename__ = 'Pagamento_'  

    id_Pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # CORREÇÃO: Usando Numeric(10, 2) no lugar de db.Decimal(10, 2)
    Valor = db.Column(Numeric(10, 2), nullable=False)
    
    Data_Pagamento = db.Column(db.Date, nullable=False)
    Metodo = db.Column(db.String(50), nullable=False)
    
    # Usando db.Enum para mapear o tipo ENUM do MySQL
    Status_Pagamento = db.Column(db.Enum('Pago', 'Pendente', name='status_pagamento_enum'), nullable=False)

    def __repr__(self):
        return f"<Pagamento id={self.id_Pagamento} valor={self.Valor} status={self.Status_Pagamento}>"