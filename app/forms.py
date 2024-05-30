from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor elige otro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese correo electrónico ya está en uso. Por favor elige otro.')

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    due_date = DateField('Fecha de Vencimiento (AAAA-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    priority = SelectField('Prioridad', choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')], validators=[DataRequired()])
    submit = SubmitField('Publicar')

class CommentForm(FlaskForm):
    content = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Agregar Comentario')
