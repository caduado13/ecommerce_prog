from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    FloatField, TextAreaField, SelectField, SelectMultipleField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models.user import User
from app.models.role import Role
import re

def validate_password_strength(form, field):
    password = field.data
    # Regex: Mínimo de 8 caracteres, pelo menos uma letra maiúscula, uma minúscula, um dígito e um caractere especial
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    if not re.fullmatch(regex, password):
        raise ValidationError(
            'A senha deve ter no mínimo 8 caracteres, '
            'incluir uma letra maiúscula, uma minúscula, '
            'um número e um caractere especial (@$!%*?&).'
        )

class RegisterForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=8, max=128)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11, message='CPF deve ter 11 dígitos.')])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8), validate_password_strength])
    confirm_password = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já foi cadastrado. Escolha outro')

    def validade_cpf(self, cpf):
        user = User.query.filter_by(cpf=cpf.data).first()
        if user:
            raise ValidationError('Esse CPF já está cadastrado')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ProductForm(FlaskForm):
    name = StringField('Nome do Produto', validators=[DataRequired(), Length(min=1, max=100)])
    price = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Descrição', validators=[Length(max=500)])
    submit = SubmitField('Salvar Produto')


class OrderStatusForm(FlaskForm):
    status = SelectField(
        'Status do Pedido',
        choices=[('novo', 'Novo'), ('processando', 'Processando'),
                 ('enviado', 'Enviado'), ('cancelado', 'Cancelado')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Atualizar Status')


class UserForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=8, max=128)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # No __init__ do view, você deve popular form.roles.choices:
    # form.roles.choices = [(r.id, r.name) for r in Role.query.all()]
    roles = SelectMultipleField('Papéis', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar Usuário')