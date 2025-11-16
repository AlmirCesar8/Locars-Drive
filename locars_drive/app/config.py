import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = "chave-super-secreta"
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gabriel:D2Y4GSarc3yB@localhost:3306/LocarsDrives"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# -------------------------
#  SEGURANÇA
# -------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "devkey123")
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY", "csrf-dev-123")

# -------------------------
#  BANCO DE DADOS SQLite
# -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "instance", "locars.db")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
