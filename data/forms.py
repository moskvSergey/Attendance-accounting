from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('ФИО', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    submit_reg = SubmitField('Зарегистрироваться')


class PersonForm(FlaskForm):
    name = StringField('ФИО')
    photo = FileField('Фото')
    submit = SubmitField('Применить')

class LessonForm(FlaskForm):
    teacher_id = StringField('Номер учителя')
    group_id = StringField('Ночер группы')
    submit = SubmitField('Применить')

class GroupForm(FlaskForm):
    name = StringField('Название')
    submit = SubmitField('Применить')