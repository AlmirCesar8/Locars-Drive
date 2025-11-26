# app/routes/administrador.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models.veiculo import Veiculo 
from app.models.usuario import Usuario # Para checar permissão
from app.formularios import VeiculoForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user # Importante para autenticação e permissão
from datetime import datetime

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin', template_folder='../templates/admin')

# ******************************************************
# Módulo de Cadastro de Veículos
# ******************************************************

@admin_bp.route('/veiculos/adicionar', methods=['GET', 'POST'])
@login_required 
def adicionar_veiculo():
    # Verificação de permissão de administrador 
    if not current_user.is_admin:
        flash("Acesso não autorizado. Apenas administradores podem cadastrar veículos.", 'error')
        return redirect(url_for('veiculos.veiculos'))
        
    form = VeiculoForm()
    
    ano_maximo = datetime.now().year + 1
    
    if form.validate_on_submit():
        # QuerySelectField retorna o objeto (Marca, Modelo, Categoria).
        # Usamos o atributo id_Marca/id_Modelo/id_Categoria para a Foreign Key.
        
        # O QuerySelectField é validado, garantindo que o objeto não é None.
        fk_marca_id = form.fk_marca_id_marca.data
        fk_modelo_id = form.fk_modelo_id_modelo.data
        fk_categoria_id = form.fk_categoria_id_categoria.data

        novo_veiculo = Veiculo(
            Frota=form.frota.data,
            Placa=form.placa.data.upper(),
            Km_Rodado=form.km_rodado.data,
            StatusVeiculo=form.status_veiculo.data,
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
            
    return render_template('adicionar_veiculo.html', form=form, title='Adicionar Novo Veículo', ano_maximo=ano_maximo)

@admin_bp.route('/painel')
@login_required 
def painel():
    if not current_user.is_admin: # <-- 2. USAR current_user.is_admin
        flash("Acesso não autorizado. Apenas administradores podem cadastrar veículos.", 'error')
        return redirect(url_for('veiculos.veiculos'))
        
    # Rota para o painel que contém o botão de adicionar veículo
    # Você pode passar dados relevantes para o painel aqui
    return render_template('painel.html', title='Painel Administrativo')