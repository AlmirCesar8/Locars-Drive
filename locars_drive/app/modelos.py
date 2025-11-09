from flask_login import UserMixin
from datetime import datetime
from app.extensions import db  # usa a extensão global configurada no __init__.py

# -------------------------------------------------------
# Modelo de Usuário
# -------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'usuario_'  # Nome da tabela no banco de dados

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Chave primária
    email = db.Column(db.String(255), nullable=False, unique=True)  # Email único
    nome_completo = db.Column(db.String(255))  # Nome completo
    senha = db.Column(db.String(255), nullable=False)  # Senha
    data_nasc = db.Column(db.Date, nullable=False)  # Data de nascimento
    cpf = db.Column(db.String(11), nullable=False, unique=True)  # CPF único
    cnh = db.Column(db.String(11), nullable=False, unique=True)  # CNH única
    cargo = db.Column(db.String(255), nullable=False)  # Cargo
    salario = db.Column(db.Numeric(10, 2), default=0.00)  # Salário
    fk_funcao_id_funcao = db.Column(db.Integer)  # Chave estrangeira para função
    fk_cidade_id_cidade = db.Column(db.Integer)  # Chave estrangeira para cidade

    def __repr__(self):
        return f'<Usuario {self.nome_completo}>'

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
