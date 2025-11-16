from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Categoria
# -------------------------------------------------------

class Categoria(db.Model):
    __tablename__ = 'Categoria'
    
    id_Categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Tipos_Categorias = db.Column(db.String(255), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Categoria id={self.id_Categoria} tipo={self.Tipos_Categorias}>"