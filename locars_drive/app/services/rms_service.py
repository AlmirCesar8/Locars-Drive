# app/services/rms_service.py

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from decimal import Decimal # Importado para precisão em cálculos financeiros
import math # Para arredondamento de dias

# Importar as classes ORM necessárias
from app.models.veiculo import Veiculo
from app.models.aluguel import Aluguel
from app.models.usuario import Usuario
from app.models.vistoria import Vistoria # Adicionado para uso na vistoria

# --- CONSTANTES DE NEGÓCIO (Ajuste conforme suas regras) ---
TAXA_REABASTECIMENTO = Decimal('50.00') # R$ por ponto percentual (0.01) abaixo do nível inicial
KM_LIMITE_POR_DIA = Decimal('100')      # Limite de KM por dia de locação
MULTA_POR_KM_EXTRA = Decimal('0.75')    # R$ por KM excedente
MULTA_DANO_FIXA = Decimal('300.00')     # Taxa mínima de processamento por dano não reportado

# ==============================================================================
# --- FUNÇÃO 1: VERIFICAÇÃO DE DISPONIBILIDADE (RMS) ---
# ==============================================================================

def verificar_disponibilidade_veiculo(session: Session, fk_veiculo_id: int, data_inicio: datetime, data_fim: datetime) -> tuple[bool, str]:
    """
    Verifica se um veículo está disponível para locação no período solicitado.
    """
    
    veiculo_status = session.query(Veiculo.StatusVeiculo).filter(Veiculo.id_Veiculo == fk_veiculo_id).scalar()
    
    if veiculo_status == 'Indisponível':
        return False, "Veículo com status 'Indisponível' no cadastro."

    conflitos = session.query(Aluguel).filter(
        and_(
            Aluguel.fk_veiculo_id == fk_veiculo_id,
            Aluguel.status.in_(['Reservado', 'Ativo']),
            
            # Lógica de Sobreposição de Períodos:
            or_(
                # A: Novo período começa dentro do existente
                Aluguel.data_retirada.between(data_inicio, data_fim),
                # B: Novo período termina dentro do existente
                Aluguel.data_devolucao_prevista.between(data_inicio, data_fim),
                # C: Existente engloba o novo período
                and_(
                    Aluguel.data_retirada <= data_inicio,
                    Aluguel.data_devolucao_prevista >= data_fim
                )
            )
        )
    ).all()

    if conflitos:
        conflito_ids = [c.id_aluguel for c in conflitos]
        return False, f"Conflito de datas. O veículo está reservado/ativo. ID(s) em conflito: {conflito_ids}"
    
    return True, "Veículo disponível."


# ==============================================================================
# --- FUNÇÃO 2: VERIFICAÇÃO DE RISCO (QUALIDADE E RISCO) ---
# ==============================================================================

def verificar_risco_cliente(session: Session, fk_usuario_id: int) -> tuple[bool, str]:
    """
    Avalia o score de reputação do cliente antes de confirmar a reserva.
    """
    score = session.query(Usuario_.Pontuacao_Reputacao).filter(Usuario_.id_Usuario == fk_usuario_id).scalar()
    
    if score is None:
        return True, "Cliente novo, sem score de risco registrado."
        
    if score < 3.5:
        return False, f"Risco alto! Cliente com reputação {score}. Requer aprovação gerencial."
    elif score < 4.0:
        return True, f"Risco moderado. Score {score}. Monitorar locação."
    else:
        return True, f"Risco baixo. Score {score}."


# ==============================================================================
# --- FUNÇÃO 3: CÁLCULO DE TARIFA (FINANÇAS) ---
# ==============================================================================

def calcular_tarifa_total(diaria_base: float, data_inicio: datetime, data_fim: datetime) -> float:
    """
    Calcula o valor total previsto da locação ou o valor de multa por atraso (em diárias).
    """
    
    delta = data_fim - data_inicio
    dias = delta.total_seconds() / (60 * 60 * 24)
    # Arredonda para cima (cobre frações de dia como dia inteiro)
    dias_cobranca = max(1, math.ceil(dias))
    
    valor_total = diaria_base * dias_cobranca
    
    return float(valor_total)


# ==============================================================================
# --- FUNÇÃO 4: CÁLCULO DE COBRANÇA EXTRA (NOVO) ---
# ==============================================================================

def calcular_cobranca_extra(session: Session, aluguel: Aluguel, vistoria_checkin: Vistoria) -> Decimal:
    """
    Calcula as multas por combustível, KM excedente e avarias no check-in.
    """
    cobranca_total = Decimal('0.00')
    
    # 1. Obter Vistoria de Check-out para comparação
    vistoria_checkout = session.query(Vistoria).filter(
        Vistoria.fk_aluguel_id == aluguel.id_aluguel,
        Vistoria.tipo == 'Check-out'
    ).first()
    
    # Se não houver check-out, assumimos o veículo no estado perfeito/full
    if not vistoria_checkout:
        return Decimal('0.00')
        
    # --- A. COBRANÇA POR COMBUSTÍVEL ---
    
    nivel_inicial = Decimal(str(vistoria_checkout.nivel_combustivel))
    nivel_final = Decimal(str(vistoria_checkin.nivel_combustivel))
    
    if nivel_final < nivel_inicial:
        # Calcula a diferença percentual (ex: 0.10) e cobra por ponto percentual
        diferenca_combustivel = nivel_inicial - nivel_final
        multa_combustivel = diferenca_combustivel * TAXA_REABASTECIMENTO
        cobranca_total += multa_combustivel
        
    # --- B. COBRANÇA POR KM EXCEDENTE ---
    
    km_inicial = Decimal(str(vistoria_checkout.quilometragem))
    km_final = Decimal(str(vistoria_checkin.quilometragem))
    km_percorrido = km_final - km_inicial
    
    # Calcula a duração da locação em dias inteiros
    delta = aluguel.data_devolucao_prevista - aluguel.data_retirada
    dias_locacao = Decimal(max(1, math.ceil(delta.total_seconds() / (60 * 60 * 24))))
    
    km_permitido = dias_locacao * KM_LIMITE_POR_DIA
    
    if km_percorrido > km_permitido:
        km_excedente = km_percorrido - km_permitido
        multa_km = km_excedente * MULTA_POR_KM_EXTRA
        cobranca_total += multa_km
        
    # --- C. COBRANÇA POR AVARIAS/DANOS ---
    
    avarias_checkin = vistoria_checkin.avarias_json 
    avarias_checkout = vistoria_checkout.avarias_json 
    
    # Lógica Simples: Se houver dano no check-in e não havia no check-out
    if avarias_checkin != avarias_checkout: 
        cobranca_total += MULTA_DANO_FIXA # Taxa fixa
        
    return cobranca_total


# ==============================================================================
# --- FUNÇÃO 5: ATUALIZAÇÃO DE REPUTAÇÃO  ---
# ==============================================================================

def atualizar_reputacao_cliente(session: Session, fk_usuario_id: int, nota_recente: float):
    """
    Placeholder: Atualiza a Pontuacao_Reputacao do cliente com base na nova nota.
    Isto será implementado no próximo passo do Módulo de Qualidade e Risco.
    """
    # Lógica a ser implementada:
    # 1. Obter o cliente e a pontuação anterior.
    # 2. Calcular a nova média ponderada.
    # 3. Salvar o novo score.
    print(f"DEBUG: Reputação do usuário {fk_usuario_id} será atualizada com nota {nota_recente}.")