from flask import Blueprint, render_template

planos_bp = Blueprint('planos', __name__)

@planos_bp.route('/')
def planos():
    return render_template('planos.html')

@planos_bp.route('/assinatura')
def assinatura():
    # Página para planos por assinatura
    return render_template('assinatura.html')  # Crie esse template ou ajuste conforme necessário