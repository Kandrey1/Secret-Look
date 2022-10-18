from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class ChangePassForm(FlaskForm):
    old_pass = PasswordField("Старый пароль: ", validators=[DataRequired()])
    password = PasswordField("Новый пароль",
                             validators=[DataRequired(),
                                         Length(min=4, max=50),
                                         EqualTo('confirm',
                                                 message='Пароли должны '
                                                         'совпадать')])
    confirm = PasswordField('Повторите новый пароль')
    submit = SubmitField("Изменить пароль")


class DeleteAccountForm(FlaskForm):
    pass_for_dell = PasswordField("Введите пароль",
                                  validators=[DataRequired(),
                                              EqualTo('confirm_for_dell',
                                                      message='Пароли должны '
                                                              'совпадать')])
    confirm_for_dell = PasswordField('Повторите пароль')
    submit = SubmitField("УДАЛИТЬ АККАУНТ")
