from app.extensions import db
from sqlalchemy import Numeric, ForeignKey, Date, Integer, String

# -------------------------------------------------------
# Modelo Locação-Seguro (Tabela locacao_seguro_)
# -------------------------------------------------------
class LocacaoSeguro(db.Model):
    # CORREÇÃO CRÍTICA: O atributo deve ser __tablename__
    __tablename__ = 'locacao_seguro_'

    # CORREÇÃO: CHAVE PRIMÁRIA COMPOSTA (RESOLVE O ArgumentError)
    # id_Locacao e id_Seguro formam a chave primária composta (PK) conforme o DDL
    id_Locacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_Seguro = db.Column(db.Integer, primary_key=True, nullable=False) 

    # Demais colunas
    id_Cliente = db.Column(db.Integer, nullable=False)
    id_Veiculo = db.Column(db.Integer, nullable=False)

    # Colunas de Datas
    Data_Prevista_Devolucao = db.Column(db.Date, nullable=True) 
    Data_Devolucao = db.Column(db.Date, nullable=False)
    Data_Fim = db.Column(db.Date, nullable=False)
    Data_Inicio = db.Column(db.Date, nullable=False)

    # Colunas de Valor e Texto
    Valor_Multa = db.Column(Numeric(10, 2), default=0.00)
    Agencia_Retirada = db.Column(db.String(255), nullable=True)
    Valor = db.Column(Numeric(10, 2), nullable=False)
    
    # Chave Estrangeira para Pagamento_
    # Referencia a tabela Pagamento_
    fk_Pagamento__id_Pagamento = db.Column(db.Integer, db.ForeignKey('Pagamento_.id_Pagamento'), nullable=True)

    def __repr__(self):
        return f"<LocacaoSeguro Locacao={self.id_Locacao}, Seguro={self.id_Seguro}>"