from app.extensions import db
from sqlalchemy import Numeric, Date, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Aluguel(db.Model):
    __tablename__ = 'aluguel'

    id_aluguel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # --- Chaves Estrangeiras ---
    # Liga ao Cliente que alugou
    # Corrigido o nome da tabela para minúsculas: 'usuario_' -> 'usuario_' (usando o nome exato da sua tabela SQL)
    fk_usuario_id = db.Column(db.Integer, ForeignKey('Usuario_.id_usuario'), nullable=False)
    # Liga ao Veículo alugado
    fk_veiculo_id = db.Column(db.Integer, ForeignKey('veiculo.id_Veiculo'), nullable=False)
    
    # --- Datas da Locação ---
    data_retirada = db.Column(db.DateTime, nullable=False)
    data_devolucao_prevista = db.Column(db.DateTime, nullable=False)
    data_devolucao_real = db.Column(db.DateTime, nullable=True)
    
    # --- Valores e Status ---
    status = db.Column(db.String(50), default='Reservado', nullable=False) # Ex: Reservado, Ativo, Finalizado, Cancelado
    valor_diaria = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total_previsto = db.Column(db.Numeric(10, 2), nullable=False)
    valor_extra = db.Column(db.Numeric(10, 2), default=0.00) # Cobrança por atraso, KM, combustível, etc.

    # --- Relações ---
    # Assumindo que o nome do modelo de usuário seja 'Usuario'
    usuario = relationship('Usuario', backref='alugueis') 
    # Para evitar circular imports, deixo a definição da relação Usuario para o modelo Usuario
    veiculo = relationship('Veiculo', backref='alugueis')
    
    # Relações com os novos módulos (Vistoria, Notificação, Avaliação)
    # vistorias é definido no modelo Vistoria, notificações em Notificacao

    def __repr__(self):
        return f"<Aluguel {self.id_aluguel} - Cliente: {self.fk_usuario_id} - Status: {self.status}>"