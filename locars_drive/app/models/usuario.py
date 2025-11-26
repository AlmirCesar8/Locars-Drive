# app/models/usuario.py

from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import Numeric, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Definindo as opções de perfil para manter a consistência
PERFIS_CHOICES = [
    'locador',  # Aluga o carro do usuário (LocarsDrive)
    'alugador', # Cliente que aluga o carro (Locatário)
    'misto'     # Pode fazer ambos
]

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuario_'

    # IDs principais
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Outros campos (manter)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    nome_completo = db.Column(db.String(255), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False) # Mudança de DateTime para Date
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    cnh = db.Column(db.String(10), nullable=True, unique=True)

    # Informações de Funcionário
    id_cliente = db.Column(db.Integer, nullable=False, default=0)
    id_funcionario = db.Column(db.Integer, nullable=False, default=0)
    id_admin = db.Column(db.Integer, nullable=False, default=0)
    cargo = db.Column(db.String(100), nullable=True) # Adicionei nullable=True se não for funcionário
    Salario = db.Column(db.Numeric(10, 2), default=0.00)
    Pontuacao_Reputacao = db.Column(db.Float, default=5.0)

    # NOVO CAMPO (Do DDL): Tipo de Perfil
    tipo_perfil = db.Column(db.String(50), nullable=False, default='alugador')
    
    # --- NOVAS CHAVES ESTRANGEIRAS (FKs) ---
    
    # 1. FK para Endereco (da correção anterior, opcional para usuário)
    fk_Endereco_id_Endereco = db.Column(db.Integer, ForeignKey('Endereco.id_Endereco'), nullable=True)

    # CNH única (None é permitido)
    cnh = db.Column(db.String(11), nullable=True, unique=True)

    # Dados somente para funcionários
    cargo = db.Column(db.String(255), nullable=True)
    salario = db.Column(Numeric(10, 2), nullable=True, default=0.00)

    fk_funcao_id_funcao = db.Column(db.Integer, nullable=True)
    fk_cidade_id_cidade = db.Column(db.Integer, nullable=True)

    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Campos de Notificação (manter)
    # notif_email = db.Column(db.Boolean, default=False)
    # notif_sms = db.Column(db.Boolean, default=False)
    # notif_push = db.Column(db.Boolean, default=False)
    # notif_promos = db.Column(db.Boolean, default=False)

    # --- Relações ---
    # Relação com Endereco
    endereco = relationship('Endereco', backref='usuarios')
    # Relação com Funcao
    funcao = relationship('Funcao', backref='usuarios')
    # Relação com Permissao
    # permissao = relationship('Permissao', backref='usuarios')
    
    
    # Métodos de senha
    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    # Flask-Login
    def get_id(self):
        return str(self.id_usuario)

    @property
    def is_active(self):
        return True

    # NOVAS PROPRIEDADES PARA CHECAGEM DE PERMISSÃO
    @property
    def is_alugador(self):
        """Pode alugar veículos (cliente normal)"""
        return self.tipo_perfil in ['alugador', 'misto']

    @property
    def is_locador(self):
        """Pode cadastrar veículos e gerenciar frota"""
        return self.tipo_perfil in ['locador', 'misto']

    @property
    def is_admin(self):
        """Verifica se o usuário é administrador (campo existente)"""
        # Supondo que id_admin > 0 significa que é admin
        return self.id_admin > 0

    def __repr__(self):
        return f"<Usuario id={self.id_usuario} email={self.email} perfil={self.tipo_perfil}>"