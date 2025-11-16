from app.extensions import db
from sqlalchemy import Numeric, Date, String
# -------------------------------------------------------
# Modelo de Adicionais
# -------------------------------------------------------

class Adicionais(db.Model):
    __tablename__ = 'Adicionais'
    
    id_Adicionais = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome_Adicionais = db.Column(db.String(255), nullable=False, unique=True)
    Descricao = db.Column(db.Text)
    Disponibilidade = db.Column(db.Enum('disponivel', 'indisponivel'), nullable=False)
    
    def __repr__(self):
        return f"<Adicionais id={self.id_Adicionais} nome={self.Nome_Adicionais} disponibilidade={self.Disponibilidade}>"
    
    ### Métodos de CRUD (teste) ###
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id_):
        return Adicionais.query.get(id_)
    
    @staticmethod
    def get_all():
        return Adicionais.query.all()
    @staticmethod
    def get_by_name(name):
        return Adicionais.query.filter_by(Nome_Adicionais=name).first()
    @staticmethod
    def get_available():
        return Adicionais.query.filter_by(Disponibilidade='disponivel').all()