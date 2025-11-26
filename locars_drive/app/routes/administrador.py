# app/routes/administrador.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models.veiculo import Veiculo 
from app.models.usuario import Usuario # Para checar permissão
from app.formularios import VeiculoForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user # Importante para autenticação e permissão
from functools import wraps

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin', template_folder='../templates/admin')

# Decorador de permissão simplificado
def admin_or_locador_required(func):
    """Verifica se o usuário é Admin ou Locador antes de executar a rota."""
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (current_user.is_admin or current_user.is_locador):
            flash('Acesso negado: Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('index_bp.index')) # Assumindo uma rota 'index_bp.index'
        return func(*args, **kwargs)
    return wrapper

# ******************************************************
# Módulo de Cadastro de Veículos
# ******************************************************

@admin_bp.route('/veiculos/adicionar', methods=['GET', 'POST'])
@admin_or_locador_required # Apenas usuários com permissão podem cadastrar
def adicionar_veiculo():
    form = VeiculoForm()
    
    if form.validate_on_submit():
        # QuerySelectField retorna o objeto (Marca, Modelo, Categoria).
        # Usamos o atributo id_Marca/id_Modelo/id_Categoria para a Foreign Key.
        
        # O QuerySelectField é validado, garantindo que o objeto não é None.
        fk_marca_id = form.fk_Marca_id_Marca.data.id_Marca
        fk_modelo_id = form.fk_Modelo_id_Modelo.data.id_Modelo
        fk_categoria_id = form.fk_Categoria_id_Categoria.data.id_Categoria

        novo_veiculo = Veiculo(
            Frota=form.Frota.data,
            Placa=form.Placa.data.upper(),
            Km_Rodado=form.Km_Rodado.data,
            StatusVeiculo=form.StatusVeiculo.data,
            fk_Marca_id_Marca=fk_marca_id,
            fk_Modelo_id_Modelo=fk_modelo_id,
            fk_Categoria_id_Categoria=fk_categoria_id
        )
        
        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            flash(f'Veículo {novo_veiculo.Placa} cadastrado com sucesso!', 'success')
            # Redireciona para a lista de veículos gerenciável
            return redirect(url_for('frotas_bp.listar_veiculos_admin')) 
        except IntegrityError:
            db.session.rollback()
            flash('Erro: Placa já cadastrada ou erro de integridade do DB.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro inesperado ao cadastrar veículo: {e}', 'danger')
            
    return render_template('adicionar_veiculo.html', form=form, title='Adicionar Novo Veículo')

@admin_bp.route('/painel')
@login_required 
@admin_or_locador_required
def painel():
    # Rota para o painel que contém o botão de adicionar veículo
    # Você pode passar dados relevantes para o painel aqui
    return render_template('painel.html', title='Painel Administrativo')