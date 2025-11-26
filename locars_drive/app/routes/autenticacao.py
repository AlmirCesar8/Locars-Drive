from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from app.extensions import bcrypt, db
from app.models.usuario import Usuario
from app.models.notificacao import Notificacao
from app.formularios import LoginForm, RegistroForm


autenticacao_bp = Blueprint('autenticacao', __name__)


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------
@autenticacao_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        # Usando check_password do modelo Usuario
        if usuario and usuario.check_password(form.senha.data):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index.index'))

        flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html', form=form)


# ------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------
@autenticacao_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = RegistroForm()

    if form.validate_on_submit():

        # Uso o método set_password do modelo, que já faz o hash
        # Se você prefere usar bcrypt diretamente, é melhor usar:
        # senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        # ... e depois atribuir diretamente
        
        # Ajuste para CNH
        cnh_valor = form.cnh.data if form.tem_cnh.data == "sim" else None

        novo_usuario = Usuario(
            nome_completo=form.nome.data,
            email=form.email.data,
            
            # ATUALIZAÇÃO 1: Salvando a senha com hash (usando o método set_password)
            # Como o modelo Usuario tem set_password, é mais limpo usá-lo após a criação do objeto,
            # ou usar o método de hash externo (como você estava fazendo) e atribuir.
            # Vou manter o seu método original (bcrypt.generate_password_hash) para consistência,
            # mas vou simplificar, removendo a decodificação desnecessária (o campo é VARCHAR no modelo).
            #senha=bcrypt.generate_password_hash(form.senha.data), 

            cpf=form.cpf.data,
            data_nasc=form.data_nasc.data,
            cnh=cnh_valor,

            # ATUALIZAÇÃO 2: Salvando o tipo de perfil do formulário
            tipo_perfil=form.tipo_perfil.data,

            # Padrões para usuário recém-criado
            id_cliente=0,
            id_funcionario=0,
            id_admin=0,

            # Se for cliente/parceiro, estes campos podem ser None (assumindo que o modelo permite)
            # Nota: No seu modelo, 'cargo' e 'salario' são nullable=True, mas no formulario.py
            # eles estão com DataRequired(). É recomendável remover o DataRequired no formulario.py
            # para perfis não-funcionários. Por enquanto, passo os dados como estão no form.
            cargo=form.cargo.data, 
            salario=form.salario.data,

            fk_funcao_id_funcao=None,
            fk_endereco_id_endereco=None,

            notif_vencimento=False,
            notif_interesse=False,
            notif_promos=False
        )
        
        # Certificando-se que a senha foi hasheada (mantendo a lógica original)
        novo_usuario.set_password(form.senha.data) # Alternativa mais limpa

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('autenticacao.login'))

        except IntegrityError as e:
            db.session.rollback()
            # Tratamento de erro aprimorado
            erro_msg = str(e.orig).lower()

            if "cpf" in erro_msg:
                flash("CPF já cadastrado.", "danger")
            elif "email" in erro_msg:
                flash("E-mail já cadastrado.", "danger")
            elif "cnh" in erro_msg:
                flash("Esta CNH já está cadastrada.", "danger")
            else:
                flash(f"Erro ao criar conta: {e.orig}", "danger")
                print(f"Erro de Integridade: {e}") # Log para debug

    # Se a validação falhar (GET ou POST com erro), renderiza o formulário
    return render_template('registro.html', form=form)


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------
@autenticacao_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('plano_ativo', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index.index'))


# ------------------------------------------------------------
# PERFIL PRINCIPAL
# ------------------------------------------------------------
@autenticacao_bp.route('/perfil')
@login_required
def perfil():

    plano_salvo = session.get('plano_ativo', 'basico')

    planos_config = {
        'basico': {'nome': 'BÁSICO', 'valor': 99.90, 'beneficios': ['10% de desconto', '1 dia grátis']},
        'intermediario': {'nome': 'INTERMEDIÁRIO', 'valor': 199.90, 'beneficios': ['20% de desconto', '2 dias grátis', 'Suporte prioritário']},
        'premium': {'nome': 'PREMIUM', 'valor': 349.90, 'beneficios': ['30% de desconto', '4 dias grátis', 'Acesso a veículos premium']},
        'vip': {'nome': 'VIP', 'valor': 599.90, 'beneficios': ['40% de desconto', '7 dias grátis', 'Concierge exclusivo']}
    }

    plano_chave = plano_salvo if plano_salvo in planos_config else 'basico'
    plano_ativo = planos_config[plano_chave]

    user_data = {
        'nome': current_user.nome_completo,
        'email': current_user.email,
        'cpf': current_user.cpf,
        'data_nasc': current_user.data_nasc.strftime('%d/%m/%Y'),
        'cnh': current_user.cnh,
        'cargo': current_user.cargo,
        'salario': float(current_user.salario or 0),
        'endereco': current_user.fk_endereco_id_endereco,
        'membro_desde': current_user.data_criacao.strftime('%d/%m/%Y'),
        'plano_ativo': plano_ativo['nome'],
        'valor_plano': plano_ativo['valor'],
        'beneficios_resumo': plano_ativo['beneficios'],
        # NOVO: Adiciona o perfil ao user_data
        'tipo_perfil': current_user.tipo_perfil
    }

    return render_template('perfil.html', user_data=user_data)


# ------------------------------------------------------------
# SUBPÁGINAS DO PERFIL
# ------------------------------------------------------------
@autenticacao_bp.route('/perfil/info')
@login_required
def perfil_info():
    plano_salvo = session.get('plano_ativo', 'basico')

    planos_config = {
        'basico': {'nome': 'BÁSICO', 'valor': 99.90, 'beneficios': ['10% de desconto', '1 dia grátis']},
        'intermediario': {'nome': 'INTERMEDIÁRIO', 'valor': 199.90, 'beneficios': ['20% de desconto', '2 dias grátis', 'Suporte prioritário']},
        'premium': {'nome': 'PREMIUM', 'valor': 349.90, 'beneficios': ['30% de desconto', '4 dias grátis', 'Acesso a veículos premium']},
        'vip': {'nome': 'VIP', 'valor': 599.90, 'beneficios': ['40% de desconto', '7 dias grátis', 'Concierge exclusivo']}
    }

    plano_chave = plano_salvo if plano_salvo in planos_config else 'basico'
    plano_ativo = planos_config[plano_chave]

    user_data = {
        'nome': current_user.nome_completo,
        'email': current_user.email,
        'cpf': current_user.cpf,
        'data_nasc': current_user.data_nasc.strftime('%d/%m/%Y'),
        'cnh': current_user.cnh,
        'cargo': current_user.cargo,
        'salario': float(current_user.salario or 0),
        'endereco': current_user.fk_endereco_id_endereco,
        'membro_desde': current_user.data_criacao.strftime('%d/%m/%Y'),
        'plano_ativo': plano_ativo['nome'],
        'valor_plano': plano_ativo['valor'],
        'beneficios_resumo': plano_ativo['beneficios'],
        # NOVO: Adiciona o perfil ao user_data
        'tipo_perfil': current_user.tipo_perfil
    }

    return render_template('perfil_info.html', user_data=user_data)


@autenticacao_bp.route('/perfil/foto')
@login_required
def perfil_foto():
    return render_template('perfil_foto.html')


@autenticacao_bp.route('/perfil/seguranca')
@login_required
def perfil_seguranca():
    return render_template('perfil_seguranca.html')


@autenticacao_bp.route('/perfil/notificacoes')
@login_required
def perfil_notificacoes():
    return render_template('perfil_notificacoes.html')


@autenticacao_bp.route('/perfil/pagamentos')
@login_required
def perfil_pagamentos():
    return render_template('perfil_pagamentos.html')


@autenticacao_bp.route('/perfil/planos')
@login_required
def perfil_planos():
    return render_template('perfil_planos.html')


# ------------------------------------------------------------
# ATIVAR PLANO (CORRIGIDA)
# ------------------------------------------------------------
@autenticacao_bp.route('/ativar_plano', methods=['POST'], endpoint='ativar_plano')
@login_required
def ativar_plano():
    # Dados enviados pelo fetch()
    data = request.get_json()
    plano = data.get("plano")

    if not plano:
        return jsonify({"erro": "Plano não informado"}), 400

    valid_plans = ['basico', 'intermediario', 'premium', 'vip']
    if plano not in valid_plans:
        return jsonify({"erro": "Plano inválido"}), 400
    session['plano_ativo'] = plano

    return jsonify({"mensagem": "Plano ativado com sucesso!", "plano": plano}), 200