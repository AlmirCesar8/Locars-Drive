# from flask_login import UserMixin
# from datetime import datetime
# from app.extensions import db 
# from datetime import date 
# from werkzeug.security import generate_password_hash, check_password_hash

# # from wtforms.validators import ValidationError # Não é necessário aqui

# # -------------------------------------------------------
# # Modelo de Usuário
# # -------------------------------------------------------
# class Usuario(UserMixin, db.Model):
#     __tablename__ = 'usuario_'

#     id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     nome_completo = db.Column(db.String(255))
#     senha = db.Column(db.String(255), nullable=False)

#     # --- CAMPOS DE DADOS BÁSICOS (Membros) ---
#     data_nasc = db.Column(db.Date, nullable=False) 
#     cpf = db.Column(db.String(11), nullable=False, unique=True) 
    
#     data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

#     # --- CAMPOS OPCIONAIS/EMPREGADOS ---
#     # CNH: Mantido nullable=True para permitir cadastro inicial sem CNH.
#     cnh = db.Column(db.String(11), nullable=True, unique=True) 
#     cargo = db.Column(db.String(255), nullable=True) 
#     salario = db.Column(db.Numeric(10, 2), default=0.00)

#     # Chaves estrangeiras opcionais
#     fk_funcao_id_funcao = db.Column(db.Integer, nullable=True) 
#     fk_cidade_id_cidade = db.Column(db.Integer, nullable=True)
    
#     def get_id(self):
#         return str(self.id_usuario)

# # -------------------------------------------------------
# # Modelo de Veículo (para uso futuro)
# # -------------------------------------------------------
# class Veiculo(db.Model):
#     __tablename__ = 'veiculo'

#     id = db.Column(db.Integer, primary_key=True)
#     marca = db.Column(db.String(80), nullable=False)
#     modelo = db.Column(db.String(100), nullable=False)
#     ano = db.Column(db.Integer, nullable=False)
#     categoria = db.Column(db.String(50))
#     diaria = db.Column(db.Float, nullable=False)
#     disponivel = db.Column(db.Boolean, default=True)

#     def __repr__(self):
#         return f'<Veiculo {self.marca} {self.modelo} ({self.ano})>'

# # -------------------------------------------------------
# # Modelo de Locação (para uso futuro)
# # -------------------------------------------------------
# class Locacao(db.Model):
#     __tablename__ = 'locacao'

#     id = db.Column(db.Integer, primary_key=True)
    
#     # CRÍTICO: db.ForeignKey usa o nome da tabela ('usuario_') e o nome da PK ('id_usuario')
#     usuario_id = db.Column(db.Integer, db.ForeignKey('usuario_.id_usuario'), nullable=False)
    
#     veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
#     data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
#     data_fim = db.Column(db.DateTime)
#     valor_total = db.Column(db.Float)
#     status = db.Column(db.String(50), default='Em andamento')

#     def __repr__(self):
#         return f'<Locacao {self.id} - Usuário {self.usuario_id}>'