from app.extensions import db  # usa a extensão global configurada no __init__.py
from sqlalchemy import Numeric, Date, String
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# -------------------------------------------------------
# Modelo de Usuário
# -------------------------------------------------------
class Usuario(db.Model):
    __tablename__ = 'Usuario_'  # Nome da tabela no banco de dados

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id_Usuario
    id_cliente = db.Column(db.Integer, nullable=False)                        # id_Cliente
    id_funcionario = db.Column(db.Integer, nullable=False)                    # id_Funcionario
    id_admin = db.Column(db.Integer, nullable=False)                          # id_Admin
    email = db.Column(db.String(255), nullable=False, unique=True)            # Email único
    nome_completo = db.Column(db.String(255))                                 # Nome completo
    senha = db.Column(db.String(255), nullable=False)                         # Senha
    data_nasc = db.Column(db.Date, nullable=False)                            # Data de nascimento
    cpf = db.Column(db.String(11), nullable=False, unique=True)               # CPF único
    cnh = db.Column(db.String(11), nullable=True, unique=True)                # CNH única
    cargo = db.Column(db.String(255), nullable=False)                         # Cargo
    salario = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)      # Salário
    fk_funcao_id_funcao = db.Column(db.Integer)                               # Chave estrangeira para função
    fk_cidade_id_cidade = db.Column(db.Integer)                               # Chave estrangeira para cidade
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    pontuacao_reputacao = db.Column(db.Float, default=5.0) 
    notif_vencimento = db.Column(db.Boolean, default=False)
    notif_interesse=db.Column(db.Boolean, default=False)
    notif_promos=db.Column(db.Boolean, default=False)
    # Métodos para gestão de senhas (boa prática)
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def __repr__(self):
        return f
    def __repr__(self):
        return f"<Usuario id={self.id_usuario} email={self.email} nome={self.nome_completo} cargo={self.cargo}>"
    
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id_usuario)
    
        return f"<Usuario id={self.id_usuario} email={self.email} nome={self.nome_completo} cargo={self.cargo}>"
    
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
