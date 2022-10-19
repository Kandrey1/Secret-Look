import datetime

from app.models import db
from app.utils import Database
from app.vote.model import Vote, VoteAnswer


def test_vote_add_row(app_test, create_client_one, create_vote_one):
    """Тестирование таблицы 'vote' в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        db.session.add(new_client_1)
        db.session.commit()

        new_vote = create_vote_one

        db.session.add(new_vote)
        db.session.commit()

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title1'
    assert vote.date_start == datetime.datetime.strptime('2022-5-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-5-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
    assert vote.question == 'question1'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0


def test_vote_update_row(app_test, create_client_one, create_vote_one):
    """Обновление записи в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        db.session.add(new_client_1)
        db.session.commit()

        new_vote = create_vote_one

        db.session.add(new_vote)
        db.session.commit()

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title1'
    assert vote.date_start == datetime.datetime.strptime('2022-5-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-5-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
    assert vote.question == 'question1'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0

    with app_test.app_context():
        new_vote = Vote.query.first()
        new_vote.title = 'title2'
        new_vote.date_start = datetime.datetime.strptime('2022-6-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
        new_vote.date_end = datetime.datetime.strptime('2022-6-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
        new_vote.question = 'question2'
        new_vote.status = 'started'
        new_vote.vote_url = 'url'
        new_vote.client_finished = 1

        db.session.add(new_vote)
        db.session.commit()

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title2'
    assert vote.date_start == datetime.datetime.strptime('2022-6-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-6-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
    assert vote.question == 'question2'
    assert vote.client_id == 1
    assert Vote.query.first().status == 'started'
    assert vote.vote_url == 'url'
    assert vote.client_finished == 1


def test_vote_delete_row(app_test, create_client_one, create_client_two,
                         create_vote_two, create_vote_one):
    """Удаление записи в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        new_client_2 = create_client_two

        db.session.add_all([new_client_1, new_client_2])
        db.session.commit()

        new_vote_1 = create_vote_one
        new_vote_2 = create_vote_two

        db.session.add_all([new_vote_1, new_vote_2])
        db.session.commit()

    vote = Vote.query.first()

    assert Vote.query.count() == 2
    assert vote.title == 'title1'
    assert vote.date_start == datetime.datetime.strptime('2022-5-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-5-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
    assert vote.question == 'question1'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0

    with app_test.app_context():
        Vote.query.filter(Vote.id == 1).delete()
        db.session.commit()

    assert Vote.query.count() == 1
    assert Vote.query.first().title == 'title2'
    assert Vote.query.first().date_start == datetime.datetime.\
        strptime('2022-6-10 12:00', '%Y-%m-%d %H:%M')
    assert Vote.query.first().date_end == datetime.datetime.\
        strptime('2022-6-11 12:00', '%Y-%m-%d %H:%M')
    assert Vote.query.first().question == 'question2'
    assert Vote.query.first().client_id == 2
    assert Vote.query.first().status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0


def test_vote_answer_add_row(app_test, create_client_one, create_vote_one,
                             create_vote_answer_one):
    """Тестирование таблицы 'vote_answer' в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        db.session.add(new_client_1)
        db.session.commit()

        new_vote_1 = create_vote_one
        db.session.add(new_vote_1)
        db.session.commit()

        new_vote_answer = create_vote_answer_one

        db.session.add(new_vote_answer)
        db.session.commit()

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.answer == 'answer1'
    assert vote_answer.vote_id == 1
    assert vote_answer.number_votes == 0


def test_vote_answer_delete_row(app_test, create_client_one, create_vote_one,
                                create_vote_answer_one, create_vote_answer_two):
    """Удаление записи в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        db.session.add(new_client_1)
        db.session.commit()

        new_vote_1 = create_vote_one
        db.session.add(new_vote_1)
        db.session.commit()

        new_vote_answer_1 = create_vote_answer_one
        new_vote_answer_2 = create_vote_answer_two

        db.session.add_all([new_vote_answer_1, new_vote_answer_2])
        db.session.commit()

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 2
    assert vote_answer.answer == 'answer1'
    assert vote_answer.vote_id == 1
    assert vote_answer.number_votes == 0

    with app_test.app_context():
        VoteAnswer.query.filter(VoteAnswer.id == 1).delete()
        db.session.commit()

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.answer == 'answer2'
    assert vote_answer.vote_id == 1
    assert vote_answer.number_votes == 0


def test_vote_cascade_delete(app_test, create_client_one, create_client_two,
                             create_vote_one, create_vote_two):
    """Проверка работы каскадного удаления, при удалении vote."""
    with app_test.app_context():
        new_client_1 = create_client_one
        new_client_2 = create_client_two

        db.session.add_all([new_client_1, new_client_2])
        db.session.commit()

        new_vote_1 = create_vote_one
        new_vote_2 = create_vote_two
        db.session.add_all([new_vote_1, new_vote_2])

        new_answer_1 = VoteAnswer(answer='answ1', vote_id=1)
        new_answer_2 = VoteAnswer(answer='answ2', vote_id=1)
        new_answer_3 = VoteAnswer(answer='answ3', vote_id=2)
        new_answer_4 = VoteAnswer(answer='answ4', vote_id=2)
        new_answer_5 = VoteAnswer(answer='answ5', vote_id=1)
        db.session.add_all([new_answer_1, new_answer_2, new_answer_3,
                            new_answer_4, new_answer_5])

        db.session.commit()

    assert Vote.query.count() == 2
    assert VoteAnswer.query.count() == 5

    Database.dell(table=Vote, delete_id=2)

    assert Vote.query.count() == 1
    assert VoteAnswer.query.count() == 3
