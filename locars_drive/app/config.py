import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
#  SEGURANÇA
# -------------------------


def conectar_db():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    
    return f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"

SQLALCHEMY_DATABASE_URI = conectar_db()
SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey123")
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY", "csrf-dev-123")
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gabriel:D2Y4GSarc3yB@localhost:3306/LocarsDrives"
    SQLALCHEMY_TRACK_MODIFICATIONS = False



# -------------------------
#  BANCO DE DADOS SQLite (Configuração alternativa)
# -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "instance", "locars.db")

# A URI de SQLite abaixo está descomentada, mas se a linha 13 (conectar_db) estiver ativa, ela será sobrescrita dependendo de como você carrega a configuração.
# Se você pretende usar MySQL, mantenha a linha 13 ativa. Se for usar SQLite, comente a linha 13 e 14.
# SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False