from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from datetime import date
from wtforms.fields import DecimalField, DateTimeLocalField
from app.extensions import db
from flask_wtf.file import FileField, FileAllowed

# Importações dos modelos (necessárias para o VeiculoForm)
# NOTA: Assumo que estas importações estão corretas no seu ambiente Flask.
try:
    from app.models.marca_veiculo import MarcaVeiculo
    from app.models.modelo import Modelo
    from app.models.categoria import Categoria
    from app.models.tipo_veiculo import TipoVeiculo
except ImportError:
    # Fallback para execução em ambiente simulado, você deve garantir que esses modelos existam.
    class MockModel:
        def __init__(self, id, nome):
            self.id = id
            self.nome = nome
    
    class MarcaVeiculo(MockModel):
        id_Marca = 1
        Nome_Marca = 'Mock Marca'
        def __init__(self, id_Marca, Nome_Marca):
            self.id_Marca = id_Marca
            self.Nome_Marca = Nome_Marca
    class Modelo(MockModel):
        id_Modelo = 1
        Nome_Modelo = 'Mock Modelo'
        def __init__(self, id_Modelo, Nome_Modelo):
            self.id_Modelo = id_Modelo
            self.Nome_Modelo = Nome_Modelo
    class Categoria(MockModel):
        id_Categoria = 1
        Tipos_Categorias = 'Mock Categoria'
        def __init__(self, id_Categoria, Tipos_Categorias):
            self.id_Categoria = id_Categoria
            self.Tipos_Categorias = Tipos_Categorias


# Funções auxiliares para buscar dados do banco de dados

def get_tipos_choices():
    try:
        return [(t.id_Tipo, t.Nome_Tipo) for t in db.session.query(TipoVeiculo).all()]
    except:
        return []
    
def get_marcas_choices():
    # Busca todas as marcas do banco e formata como (id, nome)
    try:
        return [(m.id_Marca, m.Nome_Marca) for m in db.session.query(MarcaVeiculo).all()]
    except:
        return [(1, 'Marca A'), (2, 'Marca B')] # Fallback

def get_modelos_choices():
    # Busca todos os modelos do banco e formata como (id, nome)
    try:
        return [(m.id_Modelo, m.Nome_Modelo) for m in db.session.query(Modelo).all()]
    except:
        return [(1, 'Modelo X'), (2, 'Modelo Y')] # Fallback

def get_categorias_choices():
    # Busca todas as categorias do banco e formata como (id, nome)
    try:
        return [(c.id_Categoria, c.Tipos_Categorias) for c in db.session.query(Categoria).all()]

    except:
        return [(1, 'Sedan'), (2, 'SUV')] # Fallback


class RegistroForm(FlaskForm):
    # Conteúdo do seu RegistroForm original (mantido por consistência)
    nome = StringField("Nome Completo", validators=[DataRequired(), Length(max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=14, message="CPF inválido")])
    
    data_nasc = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    
    # NOVO CAMPO: Tipo de Perfil
    # 'alugador' = Cliente/Locatário (usa o carro)
    # 'locador' = Parceiro/Alugador (fornece o carro)
    # 'misto' = Ambos
    tipo_perfil = SelectField("O que você deseja fazer?", 
                              choices=[
                                  ('alugador', 'Locar Veículos (Ser Cliente/Locatário)'), 
                                  ('locador', 'Alugar Seus Veículos (Ser Parceiro/Locador)'), 
                                  ('misto', 'Ambos (Locar e Alugar)')
                              ], 
                              validators=[DataRequired()],
                              render_kw={"style": "cursor: pointer;"})
    
    tem_cnh = RadioField("Possui CNH?",
                          choices=[("sim", "Sim"), ("nao", "Não")],
                          default="nao")

    # CNH só será validada se o usuário tiver marcado "sim"
    cnh = StringField("CNH", validators=[Length(min=11, max=11, message="A CNH deve ter 11 números.")])
    cargo = StringField("Cargo", validators=[DataRequired()])
    salario = DecimalField("Salário", validators=[DataRequired()], places=2)


    senha = PasswordField("Senha",
                          validators=[DataRequired(), Length(min=6)])
    
    confirmar_senha = PasswordField("Confirmar Senha",
                                     validators=[DataRequired(), EqualTo('senha')])

    submit = SubmitField("Registrar")


    # ----- Validação de idade -----
    def validate_data_nasc(self, field):
        today = date.today()
        age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
        if age < 16:
            raise ValidationError("Você deve ter pelo menos 16 anos para se registrar.")


    # ----- Validação de CNH -----
    def validate_cnh(self, field):
        # Só valida CNH se o usuário disse que TEM
        if self.tem_cnh.data == "sim":
            if not field.data or len(field.data) != 11:
                raise ValidationError("A CNH deve ter 11 números.")
            if not field.data.isdigit():
                raise ValidationError("A CNH deve conter apenas números.")
        else:  
            # Se o usuário disse que NÃO TEM, limpa o campo CNH
            field.data = None

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


# --- Formulário de Cadastro de Veículo ---
class VeiculoForm(FlaskForm):
    frota = IntegerField("Número da Frota", validators=[DataRequired(), NumberRange(min=1)])
    placa = StringField("Placa (7 caracteres)", validators=[DataRequired(), Length(min=7, max=7)])
    km_rodado = DecimalField("Km Rodado (Inicial)", validators=[DataRequired(), NumberRange(min=0)], places=2)

    status_veiculo = SelectField("Status Inicial", choices=[
        ('Disponível', 'Disponível'),
        ('Indisponível', 'Indisponível')
    ], validators=[DataRequired()])

    fk_tipo_id_tipo = SelectField("Tipo do Veículo", coerce=int, validators=[DataRequired()])
    fk_marca_id_marca = SelectField("Marca", coerce=int, validators=[DataRequired()])
    fk_modelo_id_modelo = SelectField("Modelo", coerce=int, validators=[DataRequired()])
    fk_categoria_id_categoria = SelectField("Categoria", coerce=int, validators=[DataRequired()])


    imagem = FileField("Imagem do Veículo", validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], "Somente imagens são permitidas.")
    ])

    submit = SubmitField("Cadastrar Veículo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # IMPORTANTE → Popular o campo que estava faltando
        from app.models.tipo_veiculo import TipoVeiculo
        #self.fk_tipo_id_tipo.choices = [
            #(t.id_Tipo, t.Nome_Tipo) for t in db.session.query(TipoVeiculo).all()
        #]

        self.fk_tipo_id_tipo.choices = get_tipos_choices()

        
        self.fk_marca_id_marca.choices = get_marcas_choices()
        self.fk_modelo_id_modelo.choices = get_modelos_choices()
        self.fk_categoria_id_categoria.choices = get_categorias_choices()


# --- Formulário de Locação (Reserva) ---
class LocacaoForm(FlaskForm):
    # Campo oculto para o ID do veículo
    id_veiculo = HiddenField() 
    
    data_retirada = DateTimeLocalField("Data e Hora da Retirada", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    data_devolucao = DateTimeLocalField("Data e Hora da Devolução", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    
    # A diária não é um campo de formulário, mas será calculada na rota.
    # Adiciono um campo opcional para simular o valor da diária, que é obrigatório no modelo Aluguel
    valor_diaria = DecimalField("Valor da Diária Sugerido (R$)", validators=[DataRequired(), NumberRange(min=1)], places=2, default=100.00)
    
    submit = SubmitField("Reservar Agora")