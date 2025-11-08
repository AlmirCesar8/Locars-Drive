from flask_login import UserMixin
from datetime import datetime
from app.extensions import db  # usa a extensão global configurada no __init__.py

# -------------------------------------------------------
# Modelo de Usuário
# -------------------------------------------------------
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'  # nome explícito da tabela (boa prática)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# -------------------------------------------------------
# Modelo de Veículo (para uso futuro)
# -------------------------------------------------------
class Veiculo(db.Model):
    __tablename__ = 'veiculo'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50))
    diaria = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Veiculo {self.marca} {self.modelo} ({self.ano})>'

# -------------------------------------------------------
# Modelo de Locação (para uso futuro)
# -------------------------------------------------------
class Locacao(db.Model):
    __tablename__ = 'locacao'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    valor_total = db.Column(db.Float)
    status = db.Column(db.String(50), default='Em andamento')

    def __repr__(self):
        return f'<Locacao {self.id} - Usuário {self.usuario_id}>'
