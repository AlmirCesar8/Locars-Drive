from app.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import relationship

class Endereco(db.Model):
    # CRITÉRIO 1: O nome da tabela DEVE ser 'endereco' para a FK funcionar
    __tablename__ = 'Endereco'

    # CRITÉRIO 2: A chave primária DEVE se chamar 'id_endereco'
    id_Endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Dados de endereço
    cep = db.Column(db.String(10), nullable=False)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(255), nullable=True)
    bairro = db.Column(db.String(255), nullable=False)
    
    # RELAÇÃO INVERSA: Usada pelo `backref='usuarios'` no modelo Usuario
    # Esta relação não precisa ser definida aqui, mas é bom para consulta:
    # usuarios = relationship('Usuario', backref='endereco_obj', lazy=True)
    
    def __repr__(self):
        return f"<Endereco id={self.id_endereco} - {self.logradouro}, {self.numero}>"