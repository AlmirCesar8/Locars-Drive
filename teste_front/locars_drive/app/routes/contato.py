from flask import Blueprint, render_template

contato_bp = Blueprint('contato', __name__, template_folder='../templates')

@contato_bp.route('/contato')
def contato():
    return render_template('contato.html')
