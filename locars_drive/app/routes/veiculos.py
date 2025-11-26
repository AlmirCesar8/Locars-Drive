from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.models.veiculo import Veiculo
# from app.models.marca_veiculo import Marca_Veiculo # Não precisamos importar aqui
# from app.models.modelo import Modelo # Não precisamos importar aqui
# from app.models.categoria import Categoria # Não precisamos importar aqui
from app.formularios import VeiculoForm

veiculos_bp = Blueprint('veiculos', __name__)

# --- Placeholder de Admin ---
# Este é um placeholder, você deve implementar a função is_admin no seu modelo Usuario.
def is_admin_placeholder():
    """Verifica se o usuário logado é um administrador (Placeholder)."""
    # Exemplo simples: retorna True se o usuário estiver autenticado.
    # Em produção, você verificaria uma coluna 'is_admin' ou 'fk_Funcao_id_Funcao'
    # no modelo Usuario.
    if not current_user.is_authenticated:
        return False
    
    # Substituir por: return current_user.is_admin 
    # ou logica baseada na funcao do usuario
    return True # Por enquanto, permite que qualquer logado teste o cadastro

# Rota principal (Listagem de Veículos) - Agora com dados reais
@veiculos_bp.route('/')
def veiculos():
    # Busca todos os veículos com os relacionamentos necessários (Marca, Modelo, Categoria)
    # db.session.query(Veiculo).options(db.joinedload(Veiculo.marca), db.joinedload(Veiculo.modelo), db.joinedload(Veiculo.categoria)).all()
    # Para simplicidade, buscaremos apenas os veículos e acessaremos as relações dinamicamente nos templates
    veiculos_lista = db.session.query(Veiculo).all()
    
    # A rota 'veiculos.veiculos' renderiza 'frotas.html' para exibir a lista
    return render_template('frotas.html', 
                           veiculos=veiculos_lista,
                           # Passa a verificação de admin para o template decidir se mostra o botão
                           is_admin=is_admin_placeholder())

@veiculos_bp.route('/<int:veiculo_id>')
def detalhe_veiculo(veiculo_id):
    # Busca o veículo pelo ID com carregamento das relações para evitar N+1
    veiculo = db.session.query(Veiculo).filter(Veiculo.id_Veiculo == veiculo_id).first()
    
    if not veiculo:
        flash("Veículo não encontrado.", 'error')
        return redirect(url_for('veiculos.veiculos'))
        
    return render_template('detalhe_veiculo.html', veiculo=veiculo)


# --- NOVO: Rota de Cadastro de Veículos (CRUD - Create) ---
@veiculos_bp.route('/admin/adicionar', methods=['GET', 'POST'])
@login_required # Garante que apenas usuários logados podem acessar
def adicionar_veiculo():
    # Verificação de permissão de administrador
    if not is_admin_placeholder():
        flash("Acesso não autorizado. Apenas administradores podem cadastrar veículos.", 'error')
        return redirect(url_for('veiculos.veiculos'))
        
    form = VeiculoForm()
    
    if form.validate_on_submit():
        # Cria o novo objeto Veiculo com os dados do formulário
        novo_veiculo = Veiculo(
            Frota=form.frota.data,
            Placa=form.placa.data.upper(), # Placa em maiúsculas
            Km_Rodado=form.km_rodado.data,
            StatusVeiculo=form.status_veiculo.data,
            fk_Marca_id_Marca=form.fk_marca_id_marca.data,
            fk_Modelo_id_Modelo=form.fk_modelo_id_modelo.data,
            fk_Categoria_id_Categoria=form.fk_categoria_id_categoria.data
        )
        
        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            # CORREÇÃO: Usando a Placa ao invés de nome_completo que não existe
            flash(f'Veículo (Placa: {novo_veiculo.Placa}) cadastrado com sucesso!', 'success')
            # Redireciona para a lista de veículos após o cadastro
            return redirect(url_for('veiculos.veiculos'))
            
        except Exception as e:
            db.session.rollback()
            # Melhorando a mensagem de erro
            error_message = f'Erro ao cadastrar o veículo. Detalhe: {e}'
            if 'Duplicate entry' in str(e) and 'Placa' in str(e):
                error_message = 'Erro: Já existe um veículo com esta placa cadastrada.'
            flash(error_message, 'error')

    # Se GET ou validação falhar, renderiza o formulário
    return render_template('admin/adicionar_veiculo.html', form=form, title="Cadastrar Novo Veículo")