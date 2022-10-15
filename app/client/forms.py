from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    login = StringField("Логин: ", validators=[DataRequired(),
                                               Length(min=3, max=50)])
    email = StringField("Email: ", validators=[DataRequired(),
                                               Length(min=3, max=150),
                                               Email(message='Некорректный '
                                                             'адрес почты')])
    password = PasswordField("Пароль",
                             validators=[DataRequired(),
                                         Length(min=4, max=50),
                                         EqualTo('confirm',
                                                 message='Пароли должны '
                                                         'совпадать')])
    confirm = PasswordField('Повторите пароль')
    # todo вставить капчу
    submit = SubmitField("Зарегистрироваться")


class AuthForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    # todo remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")
