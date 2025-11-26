from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import Numeric
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Definindo as opções de perfil para manter a consistência
# Opções: 'locador' (aluga carros), 'alugador' (usa os carros), 'misto' (faz ambos)
PERFIS_CHOICES = [
    'locador',  # Aluga o carro do usuário (LocarsDrive)
    'alugador', # Cliente que aluga o carro (Locatário)
    'misto'     # Pode fazer ambos
]

class Usuario(UserMixin,db.Model):
    __tablename__ = 'Usuario_'

    # IDs principais
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Estes eram NOT NULL — agora têm default 0 (cliente)
    id_cliente = db.Column(db.Integer, nullable=False, default=0)
    id_funcionario = db.Column(db.Integer, nullable=False, default=0)
    id_admin = db.Column(db.Integer, nullable=False, default=0)

    # NOVO CAMPO: Tipo de Perfil
    # 'alugador' (apenas cliente), 'locador' (dono de frota), 'misto' (ambos)
    tipo_perfil = db.Column(db.String(50), nullable=False, default='alugador')

    # Dados do usuário
    email = db.Column(db.String(255), nullable=False, unique=True)
    nome_completo = db.Column(db.String(255))
    senha = db.Column(db.String(255), nullable=False)

    data_nasc = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)

    # CNH única (None é permitido)
    cnh = db.Column(db.String(11), nullable=True, unique=True)

    # Dados somente para funcionários
    cargo = db.Column(db.String(255), nullable=True)
    salario = db.Column(Numeric(10, 2), nullable=True, default=0.00)

    fk_funcao_id_funcao = db.Column(db.Integer, nullable=True)
    fk_cidade_id_cidade = db.Column(db.Integer, nullable=True)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Configurações de notificação
    pontuacao_reputacao = db.Column(db.Float, default=5.0)
    notif_vencimento = db.Column(db.Boolean, default=False)
    notif_interesse = db.Column(db.Boolean, default=False)
    notif_promos = db.Column(db.Boolean, default=False)

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

    # Métodos utilitários
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_):
        return Usuario.query.get(id_)

    @staticmethod
    def get_all():
        return Usuario.query.all()