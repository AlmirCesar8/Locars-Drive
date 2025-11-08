import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-super-segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///locars.db'  # Use PostgreSQL/MySQL em produção
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'outra-chave-secreta-super-segura'