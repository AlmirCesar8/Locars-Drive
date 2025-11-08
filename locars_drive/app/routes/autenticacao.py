from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.modelos import db, Usuario
from app.extensions import bcrypt
from app.formularios import LoginForm, RegistroForm

autenticacao_bp = Blueprint('autenticacao', __name__)

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


@autenticacao_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    form = RegistroForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash('E-mail já cadastrado. Tente outro.', 'warning')
        else:
            senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
            novo_usuario = Usuario(nome=form.nome.data, email=form.email.data, senha=senha_hash)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('autenticacao.login'))
    return render_template('registro.html', form=form)

@autenticacao_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)
@autenticacao_bp.route('/logout')

@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index.index'))
