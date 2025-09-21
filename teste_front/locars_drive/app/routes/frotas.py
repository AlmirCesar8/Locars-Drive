from flask import Blueprint, render_template

frotas_bp = Blueprint('frotas', __name__)

@frotas_bp.route('/')
def frotas():
    return render_template('frotas.html')
