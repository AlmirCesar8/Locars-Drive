from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField
from app.extensions import db
from app.models.notificacao import Notificacao 


notificacoes_bp = Blueprint('notificacoes', __name__, url_prefix='/notificacoes')

class MarkAllReadForm(FlaskForm):
    """Um formulário simples, necessário apenas para gerar o token CSRF."""
    submit = SubmitField('Marcar todas como lidas')

# Criação do Blueprint (ajuste o nome se necessário)
notificacoes_bp = Blueprint('notificacoes', __name__, url_prefix='/notificacoes')

# Rota GET para exibir as notificações
@notificacoes_bp.route('/', methods=['GET'])
@login_required
def notificacoes():
    # Instancia o formulário para passar ao template
    form = MarkAllReadForm() 
    
    # CHAVE DE CORREÇÃO: Usando o atributo correto da chave estrangeira do seu modelo Usuario
    user_id_to_filter = current_user.id_usuario 

    # 1. Busca todas as notificações do usuário, ordenadas: 
    #    Não lidas primeiro, depois por data mais recente.
    
    todas_notificacoes = db.session.execute(
        db.select(Notificacao)
        .filter_by(fk_usuario_id=user_id_to_filter)
        .order_by(Notificacao.lida.asc(), Notificacao.data_envio.desc())
    ).scalars().all()

    # 2. Conta quantas não foram lidas
    nao_lidas = db.session.scalar(
        db.select(db.func.count(Notificacao.id_notificacao))
        .filter_by(fk_usuario_id=user_id_to_filter, lida=False)
    )
    
    return render_template(
        'notificacoes.html', 
        notificacoes=todas_notificacoes,
        nao_lidas_count=nao_lidas,
        form=form # Passando o objeto form
    )

# Rota POST para marcar notificações como lidas
@notificacoes_bp.route('/marcar_lidas', methods=['POST'])
@login_required
def marcar_lidas():
    # Garante que o POST veio de um formulário válido (CSRF)
    form = MarkAllReadForm()
    if form.validate_on_submit():
        user_id_to_filter = current_user.id_usuario

        try:
            # Busca todas as notificações não lidas do usuário
            nao_lidas = db.session.execute(
                db.select(Notificacao)
                .filter_by(fk_usuario_id=user_id_to_filter, lida=False)
            ).scalars().all()

            for notificacao in nao_lidas:
                notificacao.lida = True
            
            db.session.commit()
            flash(f'{len(nao_lidas)} notificações marcadas como lidas.', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao marcar notificações: {e}', 'danger')
    else:
        # Se o token CSRF for inválido, o formulário não será validado
        flash('Erro de segurança: Formulário inválido.', 'danger')

    # Redireciona de volta para a página de notificações
    return redirect(url_for('notificacoes.notificacoes'))