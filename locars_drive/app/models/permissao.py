from app.extensions import db
from sqlalchemy import LargeBinary, Integer

# -------------------------------------------------------
# Modelo Permissao (Tabela Permissao)
# -------------------------------------------------------
class Permissao(db.Model):
    __tablename__ = 'Permissao'  

    # Colunas conforme o DDL
    id_Permissoes = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # CORREÇÃO: Coluna deve ser escrita com um 'l' (db.Column)
    # BLOB é mapeado como LargeBinary no SQLAlchemy
    Acoes = db.Column(LargeBinary, nullable=False)
    
    # CORREÇÃO: Coluna deve ser escrita com um 'l' (db.Column)
    Recursos_ = db.Column(LargeBinary, nullable=False)

    def __repr__(self):
        return f"<Permissao id={self.id_Permissoes}>"