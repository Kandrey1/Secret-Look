from app.vote.model import Vote, VoteAnswer
from app.models import db


def test_vote_set_status_started(app_test, create_vote_one):
    """Устанавливает статус опроса 'started'."""
    with app_test.app_context():
        new_vote = create_vote_one

        db.session.add(new_vote)
        db.session.commit()

    vote = Vote.query.first()

    assert vote.query.count() == 1
    assert vote.status == 'waiting'
    assert vote.vote_url == ''

    vote.set_status_started()

    assert Vote.query.count() == 1
    assert Vote.query.first().status == 'started'
    assert vote.vote_url == '867nv'


def test_vote_set_status_finished(app_test, create_vote_one):
    """Устанавливает статус опроса 'finished'."""
    with app_test.app_context():
        new_vote = create_vote_one

        db.session.add(new_vote)
        db.session.commit()

    vote = Vote.query.first()

    assert vote.query.count() == 1
    assert vote.status == 'waiting'

    vote.set_status_finished()

    assert Vote.query.count() == 1
    assert Vote.query.first().status == 'finished'


def test_vote_set_client_close_vote(app_test, create_vote_one):
    """Устанавливает что клиент сам завершил опрос."""
    with app_test.app_context():
        new_vote = create_vote_one

        db.session.add(new_vote)
        db.session.commit()

    assert Vote.query.first().status == 'waiting'
    assert Vote.query.first().client_finished is False

    vote = Vote.query.first()
    vote.set_client_close_vote()

    assert Vote.query.first().status == 'finished'
    assert Vote.query.first().client_finished is True


def test_vote_answer_update_number(app_test, create_vote_answer_one):
    """Увеличивает значение поля number_votes на 1."""
    with app_test.app_context():
        new_vote_answer = create_vote_answer_one

        db.session.add(new_vote_answer)
        db.session.commit()

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.number_votes == 123

    VoteAnswer.update_number(id_update=1)

    vote_answer = VoteAnswer.query.first()

    assert VoteAnswer.query.count() == 1
    assert vote_answer.number_votes == 124

    VoteAnswer.update_number(id_update=1)
    VoteAnswer.update_number(id_update=1)

    assert vote_answer.number_votes == 126
