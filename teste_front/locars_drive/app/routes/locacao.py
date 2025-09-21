from flask import Blueprint, render_template

locacao_bp = Blueprint('locacao', __name__)

@locacao_bp.route('/')
def locacao():
    return render_template('locacao.html')

@locacao_bp.route('/sem_habilitacao')
def sem_habilitacao():
    # Página específica para locação sem habilitação
    return render_template('sem_habilitacao.html')  