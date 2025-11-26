# app/models/endereco.py

from app.extensions import db
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship

# -------------------------------------------------------
# Modelo de Endereco
# -------------------------------------------------------
class Endereco(db.Model):
    __tablename__ = 'Endereco'

    id_Endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Dados de Endereço Físico (movidos de Cidade)
    CEP = db.Column(db.String(8), nullable=False)
    Logradouro = db.Column(db.String(255), nullable=False)
    Num_Casa = db.Column(db.Integer, nullable=False)
    Bairro = db.Column(db.String(255), nullable=False)
    Complemento = db.Column(db.String(50), nullable=True)

    # Chave Estrangeira para Cidade
    fk_Cidade_id_Cidade = db.Column(db.Integer, db.ForeignKey('Cidade.id_Cidade'), nullable=False)

    # Relações
    # Permite acessar a cidade a partir do endereço
    cidade = relationship('Cidade', backref='enderecos')
    
    # Relações bidirecionais (para ser acessado pelas tabelas que o referenciam)
    # agencias = relationship('Agencia', backref='endereco')
    # usuarios = relationship('Usuario', backref='endereco')

    def __repr__(self):
        return f"<Endereco id={self.id_Endereco} cep={self.CEP} logradouro={self.Logradouro}>"