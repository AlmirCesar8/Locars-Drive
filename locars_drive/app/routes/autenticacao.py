from flask import Blueprint, render_template

autenticacao_bp = Blueprint('autenticacao', __name__)

@autenticacao_bp.route('/login')
def login():
    return render_template('login.html')

@autenticacao_bp.route('/registro')
def registro():
    return render_template('registro.html')

@autenticacao_bp.route('/perfil')
def perfil():
    return render_template('perfil.html')