from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# --- ORM ---
from app.extensions import db
from app.models.aluguel import Aluguel
from app.models.veiculo import Veiculo
from app.models.usuario import Usuario
from app.formularios import LocacaoForm


# ==========================================================
# PLACEHOLDERS RMS / RISCO – você depois coloca os reais
# ==========================================================
def verificar_disponibilidade_veiculo(session, veiculo_id, data_retirada, data_devolucao):
    veiculo = session.get(Veiculo, veiculo_id)
    if veiculo and veiculo.StatusVeiculo == 'Disponível':
        return True, "Veículo disponível para o período."
    return False, "Veículo indisponível."


def verificar_risco_cliente(session, usuario_id):
    if usuario_id == 999:
        return False, "Risco alto detectado."
    return True, "Cliente aprovado no sistema de risco."


def calcular_tarifa_total(valor_diaria, data_retirada, data_devolucao):
    diff = data_devolucao - data_retirada
    dias = diff.total_seconds() / 86400
    dias = max(1, int(dias) + (1 if dias % 1 > 0 else 0))
    return round(valor_diaria * dias, 2)


# ==========================================================
# BLUEPRINT
# ==========================================================
locacao_bp = Blueprint('locacao', __name__)


# ==========================================================
# ROTA DA LISTA DE VEÍCULOS (CATÁLOGO)
# ==========================================================
@locacao_bp.route('/', methods=['GET'])
@login_required
def locacao():
    veiculos_disponiveis = Veiculo.query.filter_by(StatusVeiculo="Disponível").all()
    form = LocacaoForm()
    return render_template('locacao.html', veiculos=veiculos_disponiveis, form=form)


# ==========================================================
# ROTA DE DETALHES DO VEÍCULO
# ==========================================================
@locacao_bp.route('/detalhe/<int:veiculo_id>')
@login_required
def detalhe_veiculo(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    return render_template('detalhe_veiculo.html', veiculo=veiculo)


# ==========================================================
# ROTA QUE RECEBE O FORM DE DETALHE_VEICULO.HTML
# ==========================================================
@locacao_bp.route('/reservar', methods=['POST'])
@login_required
def reservar():
    """
    Recebe o POST do detalhe_veiculo.html
    """
    veiculo_id = request.form.get("veiculo_id")
    data_retirada = request.form.get("data_retirada")
    data_devolucao = request.form.get("data_devolucao")

    # ----------------------------
    # Validação dos dados
    # ----------------------------
    try:
        veiculo_id = int(veiculo_id)
        data_retirada = datetime.strptime(data_retirada, '%Y-%m-%dT%H:%M')
        data_devolucao = datetime.strptime(data_devolucao, '%Y-%m-%dT%H:%M')
    except:
        flash("Erro: datas inválidas.", "danger")
        return redirect(url_for("locacao.locacao"))

    if data_retirada >= data_devolucao:
        flash("A devolução deve ser depois da retirada.", "warning")
        return redirect(url_for("locacao.detalhe_veiculo", veiculo_id=veiculo_id))

    veiculo = Veiculo.query.get(veiculo_id)
    if not veiculo:
        flash("Veículo não encontrado.", "danger")
        return redirect(url_for("locacao.locacao"))

    # ----------------------------
    # Validações RMS / Risco
    # ----------------------------
    disponivel, msg_disp = verificar_disponibilidade_veiculo(
        db.session, veiculo_id, data_retirada, data_devolucao
    )
    if not disponivel:
        flash(msg_disp, "warning")
        return redirect(url_for("locacao.locacao"))

    risco_ok, msg_risco = verificar_risco_cliente(
        db.session, current_user.id_Usuario
    )

    # ----------------------------
    # Cálculo financeiro REAL usando ValorDiaria do modelo
    # ----------------------------
    diaria = veiculo.ValorDiaria or 150.00
    valor_total = calcular_tarifa_total(diaria, data_retirada, data_devolucao)

    # ----------------------------
    # Criar locação
    # ----------------------------
    try:
        nova = Aluguel(
            fk_usuario_id=current_user.id_Usuario,
            fk_veiculo_id=veiculo_id,
            data_retirada=data_retirada,
            data_devolucao_prevista=data_devolucao,
            status="Reservado",
            valor_diaria=diaria,
            valor_total_previsto=valor_total
        )

        db.session.add(nova)
        veiculo.StatusVeiculo = "Indisponível"
        db.session.commit()

        return redirect(url_for("locacao.confirmacao", aluguel_id=nova.id_aluguel))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Erro ao salvar reserva: {e}", "danger")
        return redirect(url_for("locacao.locacao"))


# ==========================================================
# PÁGINA DE CONFIRMAÇÃO
# ==========================================================
@locacao_bp.route('/confirmacao/<int:aluguel_id>')
@login_required
def confirmacao(aluguel_id):
    aluguel = Aluguel.query.get(aluguel_id)

    if not aluguel or aluguel.fk_usuario_id != current_user.id_Usuario:
        flash("Reserva não encontrada.", "danger")
        return redirect(url_for("locacao.locacao"))

    return render_template("confirmacao_reserva.html", aluguel=aluguel)

@locacao_bp.route('/sem-habilitacao')
def sem_habilitacao():
    return render_template('sem_habilitacao.html')
