from flask import Blueprint, render_template

contato_bp = Blueprint('contato', __name__)

@contato_bp.route('/')
def contato():
    return render_template('contato.html')
