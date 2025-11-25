

from datetime import datetime
from app.extensions import db 

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    titulo = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), default='info') # Ex: 'alerta', 'sucesso', 'locacao'
    lida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento de volta com o usuário (opcional, dependendo da sua estrutura)
    # user = db.relationship('User', backref=db.backref('notificacoes', lazy=True))

    def __repr__(self):
        return f"Notificacao('{self.titulo}', '{self.lida}', '{self.data_criacao}')"