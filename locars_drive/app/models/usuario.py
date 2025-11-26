from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import Numeric, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

PERFIS_CHOICES = ['locador', 'alugador', 'misto']


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario_'  # <<< Padronizado e correto

    # Identificação principal
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Dados pessoais
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    nome_completo = db.Column(db.String(255), nullable=False)
    data_nasc = db.Column(Date, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    cnh = db.Column(db.String(11), nullable=True, unique=True)

    # Perfis do sistema
    tipo_perfil = db.Column(db.String(50), nullable=False, default='alugador')

    # Identificadores internos
    id_cliente = db.Column(db.Integer, nullable=False, default=0)
    id_funcionario = db.Column(db.Integer, nullable=False, default=0)
    id_admin = db.Column(db.Integer, nullable=False, default=0)

    # Funcionário
    cargo = db.Column(db.String(255), nullable=True)
    salario = db.Column(Numeric(10, 2), nullable=True, default=0.00)

    # Pontuação
    Pontuacao_Reputacao = db.Column(db.Float, default=5.0)

    # ============================
    #          FOREIGN KEYS
    # ============================

    # FK → Endereco (CHAVE ESTRANGEIRA DEFINIDA)
    fk_endereco_id = db.Column(
        db.Integer,
        ForeignKey('Endereco.id_Endereco'),
        nullable=True
    )

    # FK → Funcao  (AGORA CORRETA!)
    fk_funcao_id = db.Column(
        db.Integer,
        ForeignKey('funcao.id_funcao'),
        nullable=True
    )

    # FK → Cidade
    fk_cidade_id_cidade = db.Column(
        db.Integer,
        ForeignKey('Cidade.id_Cidade'),
        nullable=True
    )

    # Data de criação
    data_criacao = db.Column(DateTime, nullable=False, default=datetime.utcnow)

    # ============================
    #          RELACIONAMENTOS
    # ============================

    # CORREÇÃO APLICADA AQUI: Especificamos `foreign_keys` para evitar a ambiguidade.
    endereco = relationship('Endereco', backref='usuarios', lazy=True, foreign_keys=[fk_endereco_id])

    funcao = relationship('Funcao', backref='usuarios', lazy=True, foreign_keys=[fk_funcao_id])

    cidade = relationship('Cidade', backref='usuarios', lazy=True, foreign_keys=[fk_cidade_id_cidade])

    # ============================
    #       MÉTODOS E UTILITIES
    # ============================

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def get_id(self):
        return str(self.id_usuario)

    @property
    def is_active(self):
        return True

    @property
    def is_alugador(self):
        return self.tipo_perfil in ['alugador', 'misto']

    @property
    def is_locador(self):
        return self.tipo_perfil in ['locador', 'misto']

    @property
    def is_admin(self):
        return self.id_admin > 0

    def __repr__(self):
        return f"<Usuario id={self.id_usuario} email={self.email} perfil={self.tipo_perfil}>"