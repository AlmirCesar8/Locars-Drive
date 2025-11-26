from app.extensions import db
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Notificacao(db.Model):
    __tablename__ = 'notificacao'

    id_notificacao = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # --- Chaves Estrangeiras ---
    fk_usuario_id = db.Column(
        db.Integer,
        ForeignKey('usuario_.id_usuario'),  # Nome correto da tabela e coluna
        nullable=False
    )

    fk_aluguel_id = db.Column(
        db.Integer,
        ForeignKey('aluguel.id_aluguel'),
        nullable=True
    )

    # --- Conteúdo da Notificação ---
    tipo = db.Column(db.String(50), nullable=False)  # Ex: atraso, aviso, promo
    mensagem = db.Column(db.Text, nullable=False)
    
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

    # --- Relações ---
    usuario = relationship('Usuario', backref='notificacoes')
    aluguel = relationship('Aluguel', backref='notificacoes')

    def __repr__(self):
        return f"<Notificacao {self.id_notificacao} - Tipo: {self.tipo} - Usuário: {self.fk_usuario_id}>"
