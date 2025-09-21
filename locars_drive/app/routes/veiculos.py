from flask import Blueprint, render_template

veiculos_bp = Blueprint('veiculos', __name__)

@veiculos_bp.route('/')
def veiculos():
    return render_template('veiculos.html')

@veiculos_bp.route('/<int:veiculo_id>')
def detalhe_veiculo(veiculo_id):
    return render_template('detalhe_veiculo.html', veiculo_id=veiculo_id)
