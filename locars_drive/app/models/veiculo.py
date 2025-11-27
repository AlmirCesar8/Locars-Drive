from app.extensions import db
from sqlalchemy import Numeric, Date, String, ForeignKey
from sqlalchemy.orm import relationship

# -------------------------------------------------------
# Modelo Veículo
# -------------------------------------------------------

class Veiculo(db.Model):
    __tablename__ = 'veiculo' # Explicitando o nome da tabela
    __table_args__ = {'extend_existing': True}

    id_Veiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Frota = db.Column(db.Integer, nullable=False)
    Placa = db.Column(db.String(7), unique=True, nullable=False)
    Km_Rodado = db.Column(db.Numeric(10,2), nullable=False)
    StatusVeiculo = db.Column(db.Enum('Disponível', 'Indisponível'), nullable=False)
    imagem_principal = db.Column(db.String(255))
    fk_Tipo_Veiculo_id_Tipo = db.Column(db.Integer, ForeignKey('Tipo_Veiculo.id_Tipo'), nullable=False)

    # --- Chaves Estrangeiras Adicionadas (Para suportar o formulário) ---
    # O DDL original só tinha Categoria, mas o formulário pede todos.
    fk_Marca_id_Marca = db.Column(db.Integer, ForeignKey('Marca_Veiculo.id_Marca'), nullable=True)
    fk_Modelo_id_Modelo = db.Column(db.Integer, ForeignKey('Modelo.id_Modelo'), nullable=True)
    fk_Categoria_id_Categoria = db.Column(db.Integer, ForeignKey('Categoria.id_Categoria'), nullable=False)
    
    # --- Relações ---
    categoria = relationship('Categoria', backref='veiculos')
    # Assumindo que Marca_Veiculo e Modelo são os nomes das tabelas no DB
    marca = relationship('MarcaVeiculo', backref='veiculos')
    modelo = relationship('Modelo', backref='veiculos')

    def __repr__(self):
        return f"<Veiculo id={self.id_Veiculo} placa={self.Placa} frota={self.Frota} status={self.StatusVeiculo}>"