from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app.extensions import bcrypt, db
from app.formularios import LoginForm, RegistroForm

autenticacao_bp = Blueprint('autenticacao', __name__)

# ---------------------------------------------------------
# ATIVAR PLANO (VIA AJAX/FETCH)
# ---------------------------------------------------------
@autenticacao_bp.route('/ativar_plano', methods=['POST'])
@login_required 
def ativar_plano():
    # 1. Recebe os dados JSON (plano_id)
    data = request.get_json()
    plano_id = data.get('plano_id')
    
    if plano_id:
        # 2. LÓGICA DE ATIVAÇÃO DO PLANO (Persistência na Sessão)
        # Em um projeto real, você faria:
        # current_user.plano_ativo = plano_id
        # db.session.commit()
        
        # SIMULAÇÃO: Armazena o plano ativo na sessão do Flask
        session['plano_ativo'] = plano_id
        
        print(f"Plano '{plano_id}' salvo na sessão e SIMULADAMENTE ativado.")
        
        return jsonify({
            'success': True, 
            'message': f'Plano {plano_id} ativado com sucesso!',
            'plano_ativo': plano_id
        }), 200 # Retorna um status de sucesso (200 OK)
    else:
        return jsonify({'success': False, 'message': 'ID do plano não fornecido.'}), 400

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
@autenticacao_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index.index'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html', form=form)


# ---------------------------------------------------------
# REGISTRO
# ---------------------------------------------------------
@autenticacao_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = RegistroForm()

    if form.validate_on_submit():

        # Evita emails duplicados
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash('E-mail já cadastrado. Tente outro.', 'warning')
            return redirect(url_for('autenticacao.registro'))

        # Gera hash da senha
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

        # Captura CNH corretamente
        cnh_valor = form.cnh.data if form.tem_cnh.data == "sim" else None

        # Criação do usuário no banco
        novo_usuario = Usuario(
            nome_completo=form.nome.data,
            email=form.email.data,
            senha=senha_hash,
            cpf=form.cpf.data,
            data_nasc=form.data_nasc.data,
            cnh=form.cnh.data if form.tem_cnh.data == "sim" else None,            
            cargo=form.cargo.data,          
            salario=form.salario.data,      
            fk_funcao_id_funcao=None,
            fk_cidade_id_cidade=None
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('autenticacao.login'))

    return render_template('registro.html', form=form)



# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
@autenticacao_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # Limpa a sessão do plano ativo ao sair
    session.pop('plano_ativo', None) 
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index.index'))


# ---------------------------------------------------------
# PERFIL (PÁGINA PRINCIPAL)
# ---------------------------------------------------------
@autenticacao_bp.route('/perfil')
@login_required
def perfil():
    # 1. ESCOLHE O PLANO ATIVO (lê da sessão)
    # Tenta obter o plano salvo em session['plano_ativo'], se não existir, usa 'basico'
    plano_ativo_id = session.get('plano_ativo', 'basico') 
    
    # 2. DEFINIÇÃO DOS DADOS DO PLANO (Dicionário de Configurações)
    planos_config = {
        'basico': {'nome': 'BÁSICO', 'valor': 99.90, 'beneficios': ['10% de desconto', '1 dia grátis']},
        'intermediario': {'nome': 'INTERMEDIÁRIO', 'valor': 199.90, 'beneficios': ['20% de desconto', '2 dias grátis', 'Suporte prioritário']},
        'premium': {'nome': 'PREMIUM', 'valor': 349.90, 'beneficios': ['30% de desconto', '4 dias grátis', 'Acesso a veículos premium']},
        'vip': {'nome': 'VIP', 'valor': 599.90, 'beneficios': ['40% de desconto', '7 dias grátis', 'Concierge exclusivo']}
    }

    # 3. GARANTE QUE O PLANO É VÁLIDO E ATRIBUI OS DADOS
    plano_chave = plano_ativo_id if plano_ativo_id in planos_config else 'basico'
    plano_ativo = planos_config[plano_chave]

    # 4. MONTA O DICIONÁRIO FINAL ENVIADO PARA O TEMPLATE
    user_data = {
    'nome': current_user.nome_completo,
    'email': current_user.email,
    'cpf': current_user.cpf,
    'data_nasc': current_user.data_nasc.strftime('%d/%m/%Y'),
    'cnh': current_user.cnh,
    'cargo': current_user.cargo,
    'salario': float(current_user.salario or 0),
    'cidade': current_user.fk_cidade_id_cidade,
    'membro_desde': current_user.data_criacao.strftime('%d/%m/%Y'),
    'plano_ativo': plano_ativo['nome'],
    'valor_plano': plano_ativo['valor'],
    'beneficios_resumo': plano_ativo['beneficios']
    }

    return render_template('perfil.html', user_data=user_data)


# ---------------------------------------------------------
# ROTAS DE PERFIL SECUNDÁRIAS (Sem alterações)
# ---------------------------------------------------------

@autenticacao_bp.route("/perfil/info")
@login_required
def perfil_info():
    # Esta rota foi simplificada e agora usaria o plano ativo da sessão se necessário
    return render_template("perfil_info.html", user_data=perfil_data_mock())

@autenticacao_bp.route("/perfil/foto")
@login_required
def perfil_foto():
    return render_template("perfil_foto.html")

# ... (outras rotas secundárias do perfil permanecem as mesmas)

# Função auxiliar para evitar repetição de código (usada nas rotas secundárias)
def perfil_data_mock():
    plano_ativo_id = session.get('plano_ativo', 'basico') 
    planos_config = {
        'basico': {'nome': 'BÁSICO', 'valor': 99.90, 'beneficios': ['10% de desconto', '1 dia grátis']},
        'intermediario': {'nome': 'INTERMEDIÁRIO', 'valor': 199.90, 'beneficios': ['20% de desconto', '2 dias grátis', 'Suporte prioritário']},
        'premium': {'nome': 'PREMIUM', 'valor': 349.90, 'beneficios': ['30% de desconto', '4 dias grátis', 'Acesso a veículos premium']},
        'vip': {'nome': 'VIP', 'valor': 599.90, 'beneficios': ['40% de desconto', '7 dias grátis', 'Concierge exclusivo']}
    }
    plano_chave = plano_ativo_id if plano_ativo_id in planos_config else 'basico'
    plano_ativo = planos_config[plano_chave]

    return {
        'membro_desde': '15/11/2025',
        'valido_ate': '01/12/2025',
        'plano_ativo': plano_ativo['nome'],
        'valor_plano': plano_ativo['valor'],
        'beneficios_resumo': plano_ativo['beneficios']
    }

# ... (restante das rotas secundárias, usando perfil_data_mock se precisarem de user_data)
@autenticacao_bp.route("/perfil/seguranca")
@login_required
def perfil_seguranca():
    return render_template("perfil_seguranca.html")


@autenticacao_bp.route("/perfil/notificacoes")
@login_required
def perfil_notificacoes():
    return render_template("perfil_notificacoes.html")


@autenticacao_bp.route("/perfil/pagamentos")
@login_required
def perfil_pagamentos():
    return render_template("perfil_pagamentos.html")