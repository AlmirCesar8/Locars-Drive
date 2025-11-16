from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from datetime import date
from wtforms.fields import DecimalField

class RegistroForm(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired(), Length(max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=14, message="CPF inválido")])
    
    data_nasc = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    
    # CORREÇÃO: radio button de verdade
    tem_cnh = RadioField("Possui CNH?",
                         choices=[("sim", "Sim"), ("nao", "Não")],
                         default="nao")

    # CNH só será validada se o usuário tiver marcado "sim"
    cnh = StringField("CNH (Opcional)")
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

