from flask import Blueprint, render_template

administrador_bp = Blueprint('administrador', __name__,)

@administrador_bp.route('/painel')
def painel():
    return render_template('admin/painel.html')

@administrador_bp.route('/adicionar_veiculo')
def adicionar_veiculo():
    return render_template('admin/adicionar_veiculo.html')

@administrador_bp.route('/gerenciar_usuarios')
def gerenciar_usuarios():
    return render_template('admin/gerenciar_usuarios.html')