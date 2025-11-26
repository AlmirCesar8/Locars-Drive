# app/routes/frotas.py

from flask import Blueprint, render_template, url_for
from app.models.veiculo import Veiculo
from flask_login import current_user # Para checagem de permissão

frotas_bp = Blueprint('frotas', __name__, url_prefix='/frotas')

@frotas_bp.route('/', methods=['GET'])
def listar_veiculos():
    """Página pública de frotas (Catálogo), exibe veículos disponíveis e o link para locação."""
    veiculos = Veiculo.query.filter_by(StatusVeiculo='Disponível').all()
    
    # Checagem de permissão para exibir botão/link de locação (apenas para alugadores/misto)
    pode_alugar = current_user.is_authenticated and current_user.is_alugador 
    
    return render_template('frotas.html', 
                           veiculos=veiculos, 
                           pode_alugar=pode_alugar,
                           title='Nossa Frota Disponível')

@frotas_bp.route('/gerenciar', methods=['GET'])
# Requer login para gerenciar
def listar_veiculos_admin():
    """Exibe TODOS os veículos (Admin/Gerenciamento)."""
    veiculos = Veiculo.query.all()
    # Este template deve ser um painel de gerenciamento,
    # onde o botão de adicionar veículo (em painel.html) pode ser acessado.
    return render_template('veiculos.html', veiculos=veiculos, title='Gerenciar Veículos')