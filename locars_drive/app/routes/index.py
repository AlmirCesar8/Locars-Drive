from flask import Blueprint, render_template

# Criação do Blueprint para o index
index_bp = Blueprint('index', __name__)

# Definição da rota para a página inicial
@index_bp.route('/')
def home():
    return render_template('index.html')