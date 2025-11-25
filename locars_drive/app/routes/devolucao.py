# app/routes/devolucao.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from decimal import Decimal

# --- Importações Essenciais ---
from app.extensions import db  # Assumindo o objeto SQLAlchemy
from app.models.aluguel import Aluguel
from app.models.veiculo import Veiculo
from app.models.vistoria import Vistoria
from app.models.avaliacao import AvaliacaoServico # Usada para iniciar a avaliação pós-devolução
from app.services.rms_service import (
    calcular_tarifa_total, # Reutilizar para cálculo de atraso (diária)
    calcular_cobranca_extra,
    atualizar_reputacao_cliente
)

devolucao_bp = Blueprint('devolucao', __name__)

@devolucao_bp.route('/', methods=['GET', 'POST'])
def devolucao():
    """
    Rota GET: Exibe o formulário de devolução/check-in.
    Rota POST: Processa a devolução, realiza a vistoria e o cálculo final.
    """
    
    # ROTA GET: Exibe o formulário de devolução
    if request.method == 'GET':
        locacoes_ativas = db.session.query(Aluguel).filter(Aluguel.status == 'Ativo').all()
        return render_template('devolucao.html', locacoes=locacoes_ativas)

    # ROTA POST: Processa o Check-in
    elif request.method == 'POST':
        try:
            # 1. COLETAR DADOS (Do formulário de check-in)
            aluguel_id = int(request.form.get('aluguel_id'))
            quilometragem_final = Decimal(request.form.get('quilometragem_final'))
            combustivel_final = Decimal(request.form.get('nivel_combustivel')) # 0.00 a 1.00 (Ex: 0.75)
            avarias_reportadas = request.form.get('avarias_reportadas', 'Nenhuma') # Detalhes da vistoria
            
            data_devolucao_real = datetime.now() # O momento exato do registro
            
            # 2. BUSCAR ENTIDADES
            aluguel = db.session.get(Aluguel, aluguel_id)
            if not aluguel or aluguel.status != 'Ativo':
                flash("Locação não encontrada ou já foi finalizada.", 'error')
                return redirect(url_for('devolucao.devolucao'))
                
            veiculo = aluguel.veiculo # Acesso via relacionamento ORM (se configurado)
            
            # --- 3. REGISTRAR VISTORIA DE CHECK-IN (Módulo Vistoria) ---
            nova_vistoria_checkin = Vistoria(
                fk_aluguel_id=aluguel.id_aluguel,
                tipo='Check-in',
                nivel_combustivel=combustivel_final,
                quilometragem=quilometragem_final,
                avarias_json=avarias_reportadas,
                data_vistoria=data_devolucao_real
            )
            db.session.add(nova_vistoria_checkin)
            
            # --- 4. CÁLCULO FINANCEIRO FINAL (Módulo Finanças e Cobrança) ---
            
            # A. Cálculo de Atraso
            cobranca_atraso = Decimal('0.00')
            if data_devolucao_real > aluguel.data_devolucao_prevista:
                # Calcula o valor extra de atraso
                cobranca_atraso_float = calcular_tarifa_total(
                    float(aluguel.valor_diaria), 
                    aluguel.data_devolucao_prevista, 
                    data_devolucao_real
                )
                cobranca_atraso = Decimal(str(cobranca_atraso_float))
            
            # B. Outras Cobranças Extras (KM, Combustível, Danos)
            cobranca_km_combustivel_dano = calcular_cobranca_extra(
                db.session, # Passa a sessão
                aluguel, 
                nova_vistoria_checkin
            )
            
            # Total de extras
            total_extras = cobranca_atraso + cobranca_km_combustivel_dano
            
            # --- 5. FINALIZAÇÃO DA LOCAÇÃO E ATUALIZAÇÃO DO STATUS ---
            
            aluguel.data_devolucao_real = data_devolucao_real
            aluguel.valor_extra = total_extras # Salva o valor total de extras
            aluguel.status = 'Finalizado'
            
            # Atualiza o status do Veículo para 'Disponível' e o KM
            veiculo.StatusVeiculo = 'Disponível'
            veiculo.Km_Rodado = quilometragem_final
            
            db.session.commit()
            
            # --- 6. INÍCIO DO CICLO DE REPUTAÇÃO ---
            
            # Registra o item de avaliação no banco, aguardando nota
            nova_avaliacao = AvaliacaoServico(fk_aluguel_id=aluguel_id)
            db.session.add(nova_avaliacao)
            db.session.commit()
            
            flash(f"Devolução processada com sucesso. Cobrança extra: R$ {total_extras:.2f}.", 'success')
            return redirect(url_for('devolucao.resumo_devolucao', aluguel_id=aluguel_id))
            
        except ValueError:
            flash("Erro nos dados. Certifique-se de que KM e Combustível são números válidos.", 'error')
            return redirect(url_for('devolucao.devolucao'))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Erro de banco de dados ao processar a devolução: {e}", 'error')
            return redirect(url_for('devolucao.devolucao'))

@devolucao_bp.route('/resumo/<int:aluguel_id>')
def resumo_devolucao(aluguel_id):
    """
    Exibe o resumo financeiro final da locação.
    """
    aluguel = db.session.get(Aluguel, aluguel_id)
    if not aluguel or aluguel.status != 'Finalizado':
        flash("Resumo não disponível. Locação não finalizada.", 'error')
        return redirect(url_for('devolucao.devolucao'))
    
    # Buscar vistoria de Check-in para detalhes
    vistoria_checkin = db.session.query(Vistoria).filter(
        Vistoria.fk_aluguel_id == aluguel_id, 
        Vistoria.tipo == 'Check-in'
    ).first()
    
    # Calcular total a pagar/cobrar
    valor_final = aluguel.valor_total_previsto + aluguel.valor_extra
    
    # TODO: Envio da Fatura Final (Módulo de Comunicação)
    
    return render_template('resumo_devolucao.html', 
                           aluguel=aluguel, 
                           vistoria=vistoria_checkin, 
                           valor_final=valor_final)

@devolucao_bp.route('/sem_habilitacao')
def sem_habilitacao():
    # Rota existente
    return render_template('sem_habilitacao.html')

@devolucao_bp.route('/avaliacao', methods=['POST'])
def processar_avaliacao():
    """
    Recebe a nota do serviço pós-locação e atualiza a reputação do cliente.
    """
    try:
        aluguel_id = int(request.form.get('aluguel_id'))
        nota = float(request.form.get('nota')) # Nota de 1.0 a 5.0
        
        # 1. Busca as entidades
        aluguel = db.session.get(Aluguel, aluguel_id)
        if not aluguel or aluguel.status != 'Finalizado':
            flash("Avaliação inválida. Locação não finalizada.", 'error')
            return redirect(url_for('devolucao.resumo_devolucao', aluguel_id=aluguel_id))

        # 2. Atualiza a tabela AvaliacaoServico com a nota
        avaliacao = db.session.query(AvaliacaoServico).filter_by(fk_aluguel_id=aluguel_id).first()
        if avaliacao:
            avaliacao.nota_cliente = nota
            avaliacao.data_avaliacao = datetime.now()
        else:
            flash("Avaliação não encontrada para esta locação.", 'warning')
            
        db.session.commit()

        # 3. Chama o Serviço de Atualização de Reputação (Qualidade e Risco)
        mensagem_reputacao = atualizar_reputacao_cliente(
            db.session, 
            aluguel.fk_usuario_id, 
            nota
        )
        
        flash(f"Avaliação registrada. {mensagem_reputacao}", 'success')
        
        # Redireciona para o perfil do usuário ou painel administrativo
        return redirect(url_for('perfil_routes.perfil')) 
        
    except (ValueError, SQLAlchemyError) as e:
        db.session.rollback()
        flash(f"Erro ao processar a avaliação: {e}", 'error')
        return redirect(url_for('index.index'))