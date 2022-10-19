from app.models import db
from app.vote.model import Vote, VoteAnswer

# todo проверки на исключения


# ----------------- Vote start -------------------------------------------------
def test_api_controllers_all_vote_client_post(app_test, client_test,
                                              create_client_one,
                                              create_vote_one,
                                              create_vote_three):
    """Добавление опроса клиента """
    with app_test.app_context():
        client1 = create_client_one
        db.session.add(client1)
        db.session.commit()

        token_api = client1.get_token_api()

        vote1 = create_vote_one
        vote2 = create_vote_three
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

        assert Vote.query.count() == 2
        assert VoteAnswer.query.count() == 0

    data = {"title": "title", "question": "question",
            "date_start": "2022-5-10T12:00", "date_end": "2022-5-11T12:00",
            "answers": ["answer1", "answer2", "answer3", "answer4"]}

    headers = {
        "Authorization": f"Bearer {token_api}",
        "Accept": "*/*"
    }

    response = client_test.post("/api/vote/", json=data, headers=headers)

    assert response.status_code == 200
    assert response.get_json() == {"title": "Add"}

    assert Vote.query.count() == 3
    assert VoteAnswer.query.count() == 4


def test_api_controllers_all_vote_client_get(app_test, client_test,
                                             create_client_one, create_vote_one,
                                             create_vote_three):
    """Получение списка всех опросов клиента."""
    with app_test.app_context():
        client1 = create_client_one
        db.session.add(client1)
        db.session.commit()

        token_api = client1.get_token_api()

        vote1 = create_vote_one
        vote2 = create_vote_three
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

        assert Vote.query.count() == 2
        assert Vote.query.first().title == "title1"

        headers = {
            "Authorization": f"Bearer {token_api}",
            "Accept": "*/*"
        }

        response = client_test.get("/api/vote/", headers=headers)

        assert response.status_code == 200
        assert len(response.get_json()['Опросы']) == 2
        assert response.get_json()['Опросы'][0]['id'] == 1
        assert response.get_json()['Опросы'][0]['title'] == 'title1'
        assert response.get_json()['Опросы'][1]['id'] == 2
        assert response.get_json()['Опросы'][1]['title'] == 'title3'


def test_api_controllers_vote_client_get(app_test, client_test,
                                         create_client_one, create_vote_one,
                                         create_vote_three):
    """Получение данных конкретного опроса."""
    with app_test.app_context():
        client1 = create_client_one
        db.session.add(client1)
        db.session.commit()

        token_api = client1.get_token_api()

        vote1 = create_vote_one
        vote2 = create_vote_three
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

    headers = {
        "Authorization": f"Bearer {token_api}",
        "Accept": "*/*"
    }
    assert Vote.query.count() == 2
    assert Vote.query.get(1).title == "title1"

    response = client_test.get("/api/vote/2", headers=headers)

    assert response.status_code == 200
    assert response.get_json()['title'] == "title3"
    assert response.get_json()['question'] == "question3"
    assert response.get_json()['date_start'] == '2022-06-10T12:00:00'
    assert response.get_json()['date_end'] == '2022-06-11T12:00:00'


def test_api_controllers_vote_client_delete(app_test, client_test,
                                            create_client_one, create_vote_one,
                                            create_vote_three):
    """"""
    with app_test.app_context():
        client1 = create_client_one
        db.session.add(client1)
        db.session.commit()

        token_api = client1.get_token_api()

        vote1 = create_vote_one
        vote2 = create_vote_three
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

    headers = {
        "Authorization": f"Bearer {token_api}",
        "Accept": "*/*"
    }

    data = {"mode": "delete"}

    assert Vote.query.count() == 2
    assert Vote.query.first().title == "title1"

    response = client_test.delete("/api/vote/1", json=data, headers=headers)

    assert response.status_code == 200
    assert Vote.query.count() == 1
    assert Vote.query.first().title == "title3"

# # ----------------- Vote end -------------------------------------------------
