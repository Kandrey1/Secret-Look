import datetime
import short_url

from sqlalchemy.orm import relationship

from ..models import db, ma
from app.utils import Converter


class Vote(db.Model):
    """Таблица опроса.
        create -- дата создания опроса в БД.
        title  -- заголовок
        question -- вопрос.
        date_start -- дата запуска в формате '%Y-%m-%dT%H:%M'.
        date_end -- дата окончания в формате '%Y-%m-%dT%H:%M'.
        status -- статус опроса(waiting, started, finished)
        vote_url -- уникальная короткая часть url адреса опроса.
        client_finished -- индикатор, что клиент сам завершил опрос.
        client_id -- id клиента который создал опрос.

        Методы:
            set_status_started -- Устанавливает status в значение 'started'.
            set_status_finished -- Устанавливает status в значение 'finished'.
            get_id_from_short_url -- Преобразует закодированную короткую
                                     строку в число.
            set_client_close_vote -- Устанавливает client_finished в
                                     значение True.(клиент сам завершил показ)
    """
    __tablename__ = 'vote'

    id = db.Column(db.Integer, primary_key=True)
    create = db.Column(db.DateTime, default=datetime.datetime.today())
    title = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(250), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    vote_url = db.Column(db.String(50), nullable=False)
    client_finished = db.Column(db.Boolean, default=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id',
                                                    ondelete='CASCADE'))

    rs_answer = relationship("VoteAnswer", uselist=True,  backref="answers",
                             cascade='save-update, merge, delete')

    def __init__(self, title, question, date_start, date_end, client_id):
        self.title = title
        self.question = question
        self.date_start = Converter.str_in_datetime(date_start)
        self.date_end = Converter.str_in_datetime(date_end)
        self.client_id = client_id

        self.status = 'waiting'
        self.vote_url = ''
        self.client_finished = 0

    def __repr__(self):
        return f"<{self.title}: {self.title} - {self.date_start}>"

    def set_status_started(self) -> None:
        """Устанавливает status в значение 'started'."""
        try:
            self.status = 'started'
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"ErrSet {e}")

    def set_status_finished(self) -> None:
        """Устанавливает status в значение 'finished'."""
        try:
            self.status = 'finished'
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"ErrSet {e}")

    def _get_short_url_from_id(self) -> str:
        """Преобразует self.vote_id в закодированную короткую строку."""
        return short_url.encode_url(self.id)

    @classmethod
    def get_id_from_short_url(cls, s: str) -> int:
        """Преобразует короткую строку в число."""
        return short_url.decode_url(s)

    def create_vote_url(self):
        """Преобразует id записи в короткую строку и устанавливает
            ее в vote_url.
        """
        self.vote_url = self._get_short_url_from_id()

    def set_client_close_vote(self) -> None:
        """Устанавливает client_finished в значение True.
            Означает что клиент сам завершил показ опроса.
        """
        try:
            vote = Vote.query.filter(Vote.id == self.id).first()
            vote.status = 'finished'
            self.client_finished = True
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"ErrSet {e}")


class VoteAnswer(db.Model):
    """Таблица вариантов ответов.
        answer  -- вариант ответа.
        vote_id -- id опроса к которому относится ответ.
        number_votes -- количество голосов за этот вариант.
    """
    __tablename__ = 'vote_answer'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(150), nullable=False)
    vote_id = db.Column(db.Integer, db.ForeignKey('vote.id',
                                                  ondelete='CASCADE'))
    number_votes = db.Column(db.Integer)

    def __init__(self, answer, vote_id):
        self.answer = answer
        self.vote_id = vote_id
        self.number_votes = 0

    def __repr__(self):
        return f"<{self.vote_id} : {self.answer} - {self.number_votes}>"

    @classmethod
    def update_number(cls, id_update: int) -> None:
        """Увеличивает значение поля number_votes на 1.
           :param id_update -- id ответа, значение у которого надо обновить.
           :type id_update: int
        """
        try:
            answer = cls.query.get(id_update)
            answer.number_votes += 1
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"ErrUpdate {e}")


class VoteSchema(ma.Schema):
    class Meta:
        model = Vote
        fields = ('id', 'create', 'title', 'date_start', 'date_end',
                  'question', 'vote_url', 'status', 'client_finished',
                  'client_id')


class VoteShortSchema(ma.Schema):
    class Meta:
        model = Vote
        fields = ('id', 'title', 'date_start',  'date_end', 'status',
                  'client_finished')


class VoteAnswerSchema(ma.Schema):
    class Meta:
        model = VoteAnswer
        fields = ('id', 'answer', 'vote_id', 'number_votes')
