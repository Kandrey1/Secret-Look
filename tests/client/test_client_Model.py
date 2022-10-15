from app.client.model import Client
from passlib.hash import bcrypt
from app.models import db


def test_get_token(app_test, create_client_one):
    """Возвращает токен, который содержит id клиента."""
    with app_test.app_context():
        new_client = create_client_one

        token = new_client.get_token(expire_time=12)

    assert token


def test_get_authenticate(app_test, create_client_one):
    """Аутентификация."""
    with app_test.app_context():
        new_client = create_client_one

        db.session.add(new_client)
        db.session.commit()

        assert Client.query.count() == 1
        assert Client.query.first().login == 'login1'

    test_email = 'client1@client'
    test_password = 'pass1'

    client = Client.authenticate(email=test_email, password=test_password)

    assert client.login == 'login1'
    assert client.email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)
