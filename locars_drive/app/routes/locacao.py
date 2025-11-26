from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# --- Importações dos Modelos ORM ---
from app.extensions import db 
from app.models.aluguel import Aluguel
from app.models.veiculo import Veiculo
from app.models.usuario import Usuario 
from app.formularios import LocacaoForm # Importa o novo formulário de Locação

# --- Placeholder para Serviços RMS ---
# Estes serviços precisam ser definidos em app/services/rms_service.py
# Como não tenho o arquivo, vou criar funções placeholder no topo.
def verificar_disponibilidade_veiculo(session, veiculo_id, data_retirada, data_devolucao):
    # Simulação: Sempre disponível se o status for 'Disponível'
    veiculo = session.get(Veiculo, veiculo_id)
    if veiculo and veiculo.StatusVeiculo == 'Disponível':
        return True, "Veículo disponível para o período."
    return False, "Veículo indisponível."

def verificar_risco_cliente(session, usuario_id):
    # Simulação: Cliente sempre OK, a menos que seja o ID 999
    if usuario_id == 999:
         return False, "Risco alto detectado. A locação pode ser recusada."
    return True, "Cliente aprovado no sistema de risco."

def calcular_tarifa_total(diaria_base, data_retirada, data_devolucao):
    # Cálculo simples baseado em dias
    diferenca = data_devolucao - data_retirada
    dias = diferenca.total_seconds() / (60 * 60 * 24)
    if dias < 0.1: # Mínimo de 1 hora
        dias = 1.0
        
    valor_total = diaria_base * dias
    return round(valor_total, 2)
# --- FIM: Placeholder para Serviços RMS ---

locacao_bp = Blueprint('locacao', __name__)

@locacao_bp.route('/', methods=['GET', 'POST'])
@login_required # Locação só é permitida para usuários logados
def locacao():
    """
    Trata a visualização da página de locação e o processamento do formulário de reserva.
    """
    form = LocacaoForm()
    
    # ROTA GET: Exibe o formulário e a lista de veículos
    if request.method == 'GET':
        # Busca apenas veículos disponíveis
        veiculos_disponiveis = db.session.query(Veiculo).filter(Veiculo.StatusVeiculo == 'Disponível').all()
        # Inicializa o form (o LocacaoForm é mais simples agora, a lógica de seleção de veículo é no template)
        return render_template('locacao.html', veiculos=veiculos_disponiveis, form=form)

    # ROTA POST: Processa a solicitação de Reserva
    elif request.method == 'POST':
        # O ID do veículo pode vir de um campo oculto ou do botão/card clicado
        id_Veiculo = request.form.get('id_veiculo')
        data_retirada_str = request.form.get('data_retirada')
        data_devolucao_str = request.form.get('data_devolucao')
        
        try:
            id_Veiculo = int(id_Veiculo)
            # As datas devem vir no formato adequado do input datetime-local (ex: 2025-11-20T10:00)
            data_retirada = datetime.strptime(data_retirada_str, '%Y-%m-%dT%H:%M')
            data_devolucao = datetime.strptime(data_devolucao_str, '%Y-%m-%dT%H:%M')
        
        except (TypeError, ValueError):
            flash("Erro nos dados de entrada. Verifique o ID do veículo e as datas.", 'error')
            return redirect(url_for('locacao.locacao'))
            
        # 1. VALIDAÇÃO BÁSICA
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
            return redirect(url_for('locacao.locacao')) 
        
        # B. Risco do Cliente (Qualidade e Risco)
        risco_ok, msg_risco = verificar_risco_cliente(db.session, current_user.id_Usuario)
        # Nota: O seu sistema pode bloquear a locação se o risco for crítico (risco_ok == False)
        
        # C. Cálculo Financeiro
        # PLACEHOLDER: Define uma diária fictícia, pois o modelo Veiculo não tem campo 'valor_diaria'
        diaria_base_veiculo = 150.00 
        
        valor_total_previsto = calcular_tarifa_total(
            diaria_base_veiculo, 
            data_retirada, 
            data_devolucao
        )
        
        # --- 3. CRIAR E SALVAR NOVA RESERVA ---
        try:
            nova_locacao = Aluguel(
                fk_usuario_id=current_user.id_Usuario,
                fk_veiculo_id=id_Veiculo,
                data_retirada=data_retirada,
                data_devolucao_prevista=data_devolucao,
                status='Reservado',
                valor_diaria=diaria_base_veiculo,
                valor_total_previsto=valor_total_previsto
            )
            
            db.session.add(nova_locacao)
            # Opcional: Atualizar o StatusVeiculo para 'Indisponível' imediatamente
            veiculo.StatusVeiculo = 'Indisponível' 
            db.session.commit()
            
            # --- 4. AÇÃO PÓS-SUCESSO ---
            flash(f"Reserva nº {nova_locacao.id_aluguel} criada com sucesso! Valor Previsto: R$ {valor_total_previsto:.2f}. {msg_risco}", 'success')
            
            # Redirecionar para a página de confirmação
            return redirect(url_for('locacao.confirmacao', aluguel_id=nova_locacao.id_aluguel))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro de banco de dados ao salvar a reserva. Detalhe: {e}", 'error')
            return redirect(url_for('locacao.locacao'))
            

@locacao_bp.route('/confirmacao/<int:aluguel_id>')
@login_required
def confirmacao(aluguel_id):
    """
    Exibe os detalhes da reserva recém-criada.
    """
    aluguel = db.session.get(Aluguel, aluguel_id)
    
    # Verifica se o aluguel existe e se pertence ao usuário logado
    if not aluguel or aluguel.fk_usuario_id != current_user.id_Usuario:
        flash("Reserva não encontrada ou você não tem permissão para visualizá-la.", 'error')
        return redirect(url_for('locacao.locacao'))
        
    return render_template('confirmacao_reserva.html', aluguel=aluguel)


@locacao_bp.route('/sem_habilitacao')
def sem_habilitacao():
    """
    Página informativa ou de erro para locação sem habilitação.
    """
    return render_template('sem_habilitacao.html')