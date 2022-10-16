from app.models import db
from app.vote.model import Vote
from app.vote.utils import check_access_vote, check_max_answer_vote, \
    check_max_votes_client, get_votes_count


def test_vote_check_access_vote(app_test, create_vote_one, create_vote_two):
    """Проверка доступа у пользователя к опросу."""
    with app_test.app_context():
        new_vote_1 = create_vote_one
        new_vote_2 = create_vote_two

        db.session.add_all([new_vote_1, new_vote_2])
        db.session.commit()

    assert check_access_vote(client_id=1, vote_id=Vote.query.get(1).id) is True
    assert check_access_vote(client_id=1, vote_id=Vote.query.get(2).id) is False


def test_vote_check_max_answer_vote():
    """Проверка количества ответов на опрос."""
    assert check_max_answer_vote(current_answer=7) is False
    assert check_max_answer_vote(current_answer=3) is True


def test_vote_check_max_votes_client():
    """Проверка количества опросов созданных клиентом."""
    assert check_max_votes_client(current_votes=12) is False
    assert check_max_votes_client(current_votes=9) is True
    assert check_max_votes_client(current_votes=5) is True


# def test_vote_get_votes_on_status(client_id: int, status: str) -> list:
#     """Возвращает список опросов клиента, со статусом status(параметр)."""


def test_vote_get_votes_count(app_test, create_vote_one, create_vote_two):
    """Возвращает количество опросов клиента, со статусом status(параметр)."""
    with app_test.app_context():
        new_vote_1 = create_vote_one

        db.session.add(new_vote_1)
        db.session.commit()

    assert get_votes_count(client_id=1, status='waiting') == 1
    assert get_votes_count(client_id=1, status='started') == 0
    assert get_votes_count(client_id=1, status='finished') == 0

    vote = Vote.query.get(1)
    vote.status = 'started'
    db.session.commit()

    assert get_votes_count(client_id=1, status='waiting') == 0
    assert get_votes_count(client_id=1, status='started') == 1
    assert get_votes_count(client_id=1, status='finished') == 0

    vote = Vote.query.get(1)
    vote.status = 'finished'
    db.session.commit()

    assert get_votes_count(client_id=1, status='waiting') == 0
    assert get_votes_count(client_id=1, status='started') == 0
    assert get_votes_count(client_id=1, status='finished') == 1

# def test_vote_get_id_last_vote(client_id: int) -> int:
#     """Возвращает id опроса, который создан самым последним."""
#
#
#
# def test_vote_get_result_vote(vote_id: int) -> list[dict[str, int or str]]:
#     """Возвращает словарь со статистикой по опросу."""
