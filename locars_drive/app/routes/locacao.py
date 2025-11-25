# app/routes/locacao.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# --- Importações Essenciais ---
# Ajuste conforme a sua configuração real do Flask:
from app.extensions import db  # Assumindo que o SQLAlchemy Session/db está aqui
from app.models.aluguel import Aluguel
from app.models.veiculo import Veiculo
from app.models.usuario import Usuario# Necessário para buscar o usuário e o cliente ID
from app.services.rms_service import (
    verificar_disponibilidade_veiculo, 
    verificar_risco_cliente,
    calcular_tarifa_total
)

locacao_bp = Blueprint('locacao', __name__)

@locacao_bp.route('/', methods=['GET', 'POST'])
def locacao():
    """
    Trata a visualização do catálogo e o processamento do formulário de reserva.
    """
    
    # ROTA GET: Exibe o formulário ou o catálogo de veículos
    if request.method == 'GET':
        # Você pode filtrar veículos disponíveis aqui
        veiculos_disponiveis = db.session.query(Veiculo).filter(Veiculo.StatusVeiculo == 'Disponível').all()
        return render_template('locacao.html', veiculos=veiculos_disponiveis)

    # ROTA POST: Processa a solicitação de Reserva
    elif request.method == 'POST':
        try:
            # 1. COLETAR E VALIDAR DADOS DO FORMULÁRIO
            
            # ATENÇÃO: É crucial que o usuário esteja logado. Aqui usamos um placeholder.
            # No seu sistema real, use 'current_user.id' ou similar.
            usuario_logado_id = 1 # PLACEHOLDER: ID do usuário logado (ex: João Silva)
            
            id_Veiculo= int(request.form.get('id_veiculo'))
            
            data_retirada_str = request.form.get('data_retirada')
            data_devolucao_str = request.form.get('data_devolucao')
            
            # As datas devem vir no formato adequado do input datetime-local (ex: 2025-11-20T10:00)
            data_retirada = datetime.strptime(data_retirada_str, '%Y-%m-%dT%H:%M')
            data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%dT%H:%M')
            
            if data_retirada >= data_devolucao:
                flash("A data de devolução deve ser posterior à data de retirada.", 'warning')
                return redirect(url_for('locacao.locacao'))
            
            veiculo = db.session.get(Veiculo, id_Veiculo)
            if not veiculo:
                flash("Veículo selecionado não existe.", 'error')
                return redirect(url_for('locacao.locacao'))
            
            # --- 2. CHAMAR SERVIÇOS DE VALIDAÇÃO (RMS e Risco) ---
            
            # A. Disponibilidade (RMS)
            disponivel, msg_disponibilidade = verificar_disponibilidade_veiculo(
                db.session, 
                id_Veiculo, 
                data_retirada, 
                data_devolucao
            )
            
            if not disponivel:
                flash(f"Reserva recusada: {msg_disponibilidade}", 'warning')
                return render_template('locacao.html') 
            
            # B. Risco do Cliente (Qualidade e Risco)
            risco_ok, msg_risco = verificar_risco_cliente(db.session, usuario_logado_id)
            
            if not risco_ok:
                flash(f"Reserva em Risco: {msg_risco}", 'error')
                # A lógica de bloqueio pode ser implementada aqui se o risco for CRÍTICO
            
            # C. Cálculo Financeiro
            # IMPORTANTE: Você precisa garantir que a diária base é buscada corretamente.
            # Aqui, assumimos que 'veiculo' tem um atributo 'valor_diaria' ou você busca via 'Categoria'.
            diaria_base_veiculo = 100.00  # PLACEHOLDER (Use a lógica real do seu modelo)
            
            valor_total_previsto = calcular_tarifa_total(
                diaria_base_veiculo, 
                data_retirada, 
                data_devolucao
            )
            
            # --- 3. CRIAR E SALVAR NOVA RESERVA ---
            nova_locacao = Aluguel(
                fk_usuario_id=usuario_logado_id,
                fk_veiculo_id=id_Veiculo,
                data_retirada=data_retirada,
                data_devolucao_prevista=data_devolucao,
                status='Reservado',
                valor_diaria=diaria_base_veiculo,
                valor_total_previsto=valor_total_previsto
            )
            
            db.session.add(nova_locacao)
            db.session.commit()
            
            # --- 4. AÇÃO PÓS-SUCESSO ---
            flash(f"Reserva nº {nova_locacao.id_aluguel} criada com sucesso! Valor Previsto: R$ {valor_total_previsto:.2f}. {msg_risco}", 'success')
            
            # Redirecionar para a página de confirmação
            return redirect(url_for('locacao.confirmacao', aluguel_id=nova_locacao.id_aluguel))
            
        except ValueError as e:
            flash(f"Erro no formato dos dados (Verifique datas e IDs): {e}", 'error')
            return redirect(url_for('locacao.locacao'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro de banco de dados ao salvar a reserva. Tente novamente. Detalhe: {e}", 'error')
            return redirect(url_for('locacao.locacao'))
            

@locacao_bp.route('/confirmacao/<int:aluguel_id>')
def confirmacao(aluguel_id):
    """
    Exibe os detalhes da reserva recém-criada.
    """
    aluguel = db.session.get(Aluguel, aluguel_id)
    
    if not aluguel:
        flash("Reserva não encontrada.", 'error')
        return redirect(url_for('locacao.locacao'))
        
    # TODO: Integração do Módulo de Comunicação:
    # service_notificacao.enviar_alerta(aluguel, 'Confirmação de Reserva')
    
    # Renderizar um template específico para a confirmação de reserva
    return render_template('confirmacao_reserva.html', aluguel=aluguel)


@locacao_bp.route('/sem_habilitacao')
def sem_habilitacao():
    """
    Página informativa ou de erro para locação sem habilitação.
    """
    return render_template('sem_habilitacao.html')