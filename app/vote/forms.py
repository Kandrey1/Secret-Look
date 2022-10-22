from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length, InputRequired


class VoteForm(FlaskForm):
    title = StringField("Заголовок: ", validators=[DataRequired(),
                                                   Length(min=1, max=100)])
    question = StringField("Вопрос: ", validators=[DataRequired(),
                                                   Length(min=1, max=250)])
    date_start = DateTimeLocalField("Дата запуска", format='%Y-%m-%dT%H:%M',
                                    validators=[InputRequired()])
    date_end = DateTimeLocalField("Дата окончания", format='%Y-%m-%dT%H:%M',
                                  validators=[InputRequired()])
    save_vote = SubmitField("Сохранить")
    # для ответов
    answer = StringField("Введите вариант ответа: ",
                         validators=[Length(min=1, max=100)])
    add_answer = SubmitField("Добавить")
