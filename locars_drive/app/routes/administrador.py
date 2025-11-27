# app/routes/administrador.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models.veiculo import Veiculo 
from app.models.usuario import Usuario # Para checar permissão
from app.formularios import VeiculoForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, current_user # Importante para autenticação e permissão
from datetime import datetime
from app.models.tipo_veiculo import TipoVeiculo
import os
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.veiculo import Veiculo
from app.models.tipo_veiculo import TipoVeiculo


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin', template_folder='../templates/admin')

# ******************************************************
# Módulo de Cadastro de Veículos
# ******************************************************

@admin_bp.route('/veiculos/adicionar', methods=['GET', 'POST'])
@login_required 
def adicionar_veiculo():
    # Verificação de permissão de administrador
    if not current_user.is_admin: # <-- 1. USAR current_user.is_admin
        flash("Acesso não autorizado. Apenas administradores podem cadastrar veículos.", 'error')

    form = VeiculoForm()

    if form.validate_on_submit():

        # --------------------------
        # 1. Salvar imagem (se enviada)
        # --------------------------
        imagem_nome = None
        file = form.imagem.data

        if file and file.filename:
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            from datetime import datetime

            filename = secure_filename(file.filename)
            
            # pasta: static/uploads
            base_path = current_app.root_path
            upload_folder = os.path.join(base_path, 'static', 'uploads')

            # criar pasta se não existir
            os.makedirs(upload_folder, exist_ok=True)

            # path completo
            file_path = os.path.join(upload_folder, filename)

            # salvar arquivo
            file.save(file_path)

            # nome salvo no banco
            imagem_nome = filename

        # --------------------------
        # 2. Criar objeto veículo
        # --------------------------
        novo_veiculo = Veiculo(
            Frota=form.frota.data,
            Placa=form.placa.data.upper(),
            Km_Rodado=form.km_rodado.data,
            StatusVeiculo=form.status_veiculo.data,
            fk_Tipo_Veiculo_id_Tipo=form.fk_tipo_id_tipo.data,
            fk_Marca_id_Marca=form.fk_marca_id_marca.data,
            fk_Modelo_id_Modelo=form.fk_modelo_id_modelo.data,
            fk_Categoria_id_Categoria=form.fk_categoria_id_categoria.data,
            imagem_principal=imagem_nome  # <-- AQUI O CAMPO ESTAVA FALTANDO
        )

        try:
            db.session.add(novo_veiculo)
            db.session.commit()

            flash(f'Veículo (Placa: {novo_veiculo.Placa}) cadastrado com sucesso!', 'success')
            return redirect(url_for('veiculos.veiculos'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar veículo: {e}", "error")

    return render_template('admin/adicionar_veiculo.html', form=form, title="Cadastrar Novo Veículo")

@admin_bp.route('/painel')
@login_required 
def painel():
    if not current_user.is_admin: # <-- 2. USAR current_user.is_admin
        flash("Acesso não autorizado. Apenas administradores podem cadastrar veículos.", 'error')
        return redirect(url_for('veiculos.veiculos'))
        
    # Rota para o painel que contém o botão de adicionar veículo
    # Você pode passar dados relevantes para o painel aqui
    return render_template('painel.html', title='Painel Administrativo')