from app.extensions import db
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class Notificacao(db.Model):
    __tablename__ = 'notificacao'

    id_notificacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Liga ao destinatário
    fk_usuario_id = db.Column(db.Integer, ForeignKey('Usuario_.id_usuario'), nullable=False)
    # Contexto (opcional: nem toda notificação é sobre um aluguel)
    fk_aluguel_id = db.Column(db.Integer, ForeignKey('aluguel.id_aluguel'), nullable=True)
    
    tipo = db.Column(db.String(50), nullable=False) # Ex: 'Atraso', 'Lembrete', 'Promocao'
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

    # Relação
    usuario = relationship('Usuario', backref='notificacoes')

    def __repr__(self):
        return f"<Notificacao {self.id_notificacao} - Tipo: {self.tipo} - Cliente: {self.fk_usuario_id}>"