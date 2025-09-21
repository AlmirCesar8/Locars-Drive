from flask import Blueprint, render_template

devolucao_bp = Blueprint('devolucao', __name__)

@devolucao_bp.route('/')
def devolucao():
    return render_template('devolucao.html')