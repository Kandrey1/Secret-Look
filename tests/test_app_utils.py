import datetime

from app.client.model import Client
from app.vote.model import Vote, VoteAnswer
from passlib.hash import bcrypt
from app.models import db
from app.utils import Database, Converter


# ====================== DATABASE ==============================================
# --------------------------- SAVE ---------------------------------------------


def test_database_save_client(app_test, create_client_one):
    """Сохранение записи в БД."""
    with app_test.app_context():
        new_client = create_client_one

    Database.save(row=new_client)

    client = Client.query.first()

    assert Client.query.count() == 1
    assert client.login == 'login1'
    assert client.email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)


def test_database_save_vote(app_test, create_client_one, create_vote_one):
    """Сохранение записи в БД."""
    with app_test.app_context():
        new_client = create_client_one
        db.session.add(new_client)
        db.session.commit()

        new_vote = create_vote_one

    Database.save(row=new_vote)

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title1'
    assert vote.date_start == datetime.datetime.strptime('2022-5-10 12:00',
                                                         '%Y-%m-%d %H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-5-11 12:00',
                                                       '%Y-%m-%d %H:%M')
    assert vote.question == 'question1'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0


def test_database_save_vote_answer(app_test, create_client_one, create_vote_one,
                                   create_vote_answer_one):
    """Сохранение записи в БД."""
    with app_test.app_context():
        new_client = create_client_one
        db.session.add(new_client)
        db.session.commit()

        new_vote = create_vote_one
        db.session.add(new_vote)
        db.session.commit()

        new_vote_answer = create_vote_answer_one

    Database.save(row=new_vote_answer)

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.answer == 'answer1'
    assert vote_answer.vote_id == 1
    assert vote_answer.number_votes == 0


# --------------------------- DELETE -------------------------------------------
def test_database_dell_client(app_test, create_client_one, create_client_two):
    """Удаление записи из БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        new_client_2 = create_client_two

        db.session.add_all([new_client_1, new_client_2])
        db.session.commit()

    assert Client.query.count() == 2
    assert Client.query.first().login == 'login1'
    assert Client.query.first().email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)

    Database.dell(table=Client, delete_id=1)

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login2'
    assert Client.query.first().email == 'client2@client'
    assert bcrypt.verify('pass2', Client.query.first().password)


def test_database_dell_vote(app_test, create_client_one, create_client_two,
                            create_vote_one, create_vote_two):
    """Удаление записи из БД."""
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
    assert vote.date_start == datetime.datetime.strptime('2022-5-10 12:00',
                                                         '%Y-%m-%d %H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-5-11 12:00',
                                                       '%Y-%m-%d %H:%M')
    assert vote.question == 'question1'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0

    Database.dell(table=Vote, delete_id=1)

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title2'
    assert vote.date_start == datetime.datetime.strptime('2022-6-10 12:00',
                                                         '%Y-%m-%d %H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-6-11 12:00',
                                                       '%Y-%m-%d %H:%M')
    assert vote.question == 'question2'
    assert vote.client_id == 2
    assert Vote.query.first().status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0


def test_database_dell_vote_answer(app_test, create_client_one,
                                   create_vote_one, create_vote_answer_one,
                                   create_vote_answer_two):
    """Удаление записи из БД."""
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

    Database.dell(table=VoteAnswer, delete_id=1)

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.answer == 'answer2'
    assert vote_answer.vote_id == 1
    assert vote_answer.number_votes == 0


# --------------------------- UPDATE -------------------------------------------
def test_database_update_client(app_test, create_client_one):
    """Обновление записи в БД."""
    update = {"login": "login2",
              "email": "client2@client",
              "password": "pass2"}

    with app_test.app_context():
        new_client = create_client_one

        db.session.add(new_client)
        db.session.commit()

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login1'
    assert Client.query.first().email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)

    Database.up(table=Client, update_id=1, data_update=update)

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login2'
    assert Client.query.first().email == 'client2@client'
    assert bcrypt.verify('pass2', Client.query.first().password)


def test_database_update_vote(app_test, create_client_one, create_vote_one):
    """Обновление записи в БД."""
    update = {'title': 'title2',
              'date_start': '2022-6-10T12:00',
              'date_end': '2022-6-11T12:00',
              'question': 'question2',
              'client_id': 1}

    with app_test.app_context():
        new_client = create_client_one
        db.session.add(new_client)
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

    Database.up(table=Vote, update_id=1, data_update=update)

    vote = Vote.query.first()

    assert Vote.query.count() == 1
    assert vote.title == 'title2'
    assert vote.date_start == datetime.datetime.strptime('2022-6-10T12:00',
                                                         '%Y-%m-%dT%H:%M')
    assert vote.date_end == datetime.datetime.strptime('2022-6-11T12:00',
                                                       '%Y-%m-%dT%H:%M')
    assert vote.question == 'question2'
    assert vote.client_id == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''
    assert vote.client_finished == 0


# ====================== CONVERT ===============================================
def test_convert_str_in_datetime():
    """Преобразует дату в формате строки в объект datetime."""
    res = Converter.str_in_datetime('2022-6-10T12:00')

    assert res == datetime.datetime.strptime('2022-6-10T12:00',
                                             '%Y-%m-%dT%H:%M')


def test_convert_datetime_in_str():
    """Преобразует date_time_obj объект datetime в строку."""
    date = datetime.datetime.strptime('2022-6-10T12:00', '%Y-%m-%dT%H:%M')

    res = Converter.datetime_in_str(date)

    assert res == '2022-06-10T12:00'
