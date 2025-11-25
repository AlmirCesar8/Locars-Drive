from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
# Importação NECESSÁRIA para buscar as notificações
from app.models.notificacao import Notificacao 
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
            fk_cidade_id_cidade=None,
            # Campos de notificação (assumindo default False se não forem preenchidos)
            notif_vencimento=False,
            notif_interesse=False,
            notif_promos=False
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
    # Nota: Assumindo que current_user tem todos os campos necessários (nome_completo, email, cpf, etc.)
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
# PERFIL NOTIFICAÇÕES (Lógica GET e POST atualizada)
# ---------------------------------------------------------
@autenticacao_bp.route('/perfil/notificacoes', methods=['GET', 'POST'])
@login_required
def perfil_notificacoes():
    # Lógica POST para salvar preferências
    if request.method == 'POST':
        try:
            # Garante que os valores booleanos são salvos corretamente
            current_user.notif_vencimento = 'notificacao_vencimento' in request.form
            current_user.notif_interesse = 'notificacao_interesse' in request.form
            current_user.notif_promos = 'notificacao_promos' in request.form
            
            db.session.commit()
            flash('Preferências de notificação salvas com sucesso.', 'success')
            # Redireciona para evitar reenvio do formulário
            return redirect(url_for('autenticacao.perfil_notificacoes')) 
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar preferências: {e}', 'danger')
            return redirect(url_for('autenticacao.perfil_notificacoes'))

    # Lógica GET para exibir a página (busca as notificações)
    
    try:
        # Busca todas as notificações do usuário logado, ordenadas pela data mais recente
        # Nota: Assegure-se que Notificacao.fk_usuario_id e current_user.id_Usuario são os campos corretos
        notificacoes_usuario = db.session.query(Notificacao).filter(
            Notificacao.fk_usuario_id == current_user.id_Usuario 
        ).order_by(Notificacao.DataNotificacao.desc()).all()
        
    except Exception as e:
        flash('Não foi possível carregar suas notificações.', 'danger')
        notificacoes_usuario = []
        print(f"Erro ao buscar notificações: {e}")

    # Renderiza o template, passando a lista de notificações
    return render_template(
        'perfil_notificacoes.html', 
        notificacoes=notificacoes_usuario
    )

# ---------------------------------------------------------
# MARCAR NOTIFICAÇÃO COMO LIDA (NOVA ROTA AJAX)
# ---------------------------------------------------------
@autenticacao_bp.route('/notificacoes/marcar_lida/<int:notificacao_id>', methods=['POST'])
@login_required
def marcar_lida(notificacao_id):
    try:
        notificacao = db.session.query(Notificacao).filter_by(
            id_Notificacao=notificacao_id, 
            fk_usuario_id=current_user.id_Usuario
        ).first()

        if notificacao:
            notificacao.Lida = True
            db.session.commit()
            return jsonify({'success': True, 'message': 'Notificação marcada como lida.'}), 200
        else:
            return jsonify({'success': False, 'message': 'Notificação não encontrada ou não pertence ao usuário.'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao marcar notificação como lida: {e}")
        return jsonify({'success': False, 'message': 'Erro interno ao processar a requisição.'}), 500


# ---------------------------------------------------------
# ROTAS DE PERFIL SECUNDÁRIAS (Mantidas com pequenas correções)
# ---------------------------------------------------------

# Função auxiliar para evitar repetição de código (usada nas rotas secundárias)
def perfil_data_mock():
    # Esta função precisa ser adaptada para usar current_user se for usada em templates reais
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
        # Usando dados reais do current_user sempre que possível
        'nome': current_user.nome_completo,
        'email': current_user.email,
        'membro_desde': current_user.data_criacao.strftime('%d/%m/%Y'),
        'valido_ate': '01/12/2025', # Mock, pois o vencimento do plano não está no modelo
        'plano_ativo': plano_ativo['nome'],
        'valor_plano': plano_ativo['valor'],
        'beneficios_resumo': plano_ativo['beneficios']
    }


@autenticacao_bp.route("/perfil/info")
@login_required
def perfil_info():
    # Passa dados mockados (e reais) para o template
    return render_template("perfil_info.html", user_data=perfil_data_mock())

@autenticacao_bp.route("/perfil/foto")
@login_required
def perfil_foto():
    return render_template("perfil_foto.html")


@autenticacao_bp.route("/perfil/seguranca")
@login_required
def perfil_seguranca():
    return render_template("perfil_seguranca.html")


# Nota: perfil_notificacoes foi movida e atualizada acima


@autenticacao_bp.route("/perfil/pagamentos")
@login_required
def perfil_pagamentos():
    return render_template("perfil_pagamentos.html")