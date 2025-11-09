from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

def conectar():
    return f'mysql+pymysql://{username}:{password}@{hostname}/{database}'

SQLALCHEMY_DATABASE_URI = conectar()
SQLALCHEMY_TRACK_MODIFICATIONS = False