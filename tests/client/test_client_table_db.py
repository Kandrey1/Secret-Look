import pytest
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.client.model import Client


def test_add_row(app_test, create_client_one):
    """Тестирование таблицы 'client' в БД."""
    with app_test.app_context():
        new_client = create_client_one

        db.session.add(new_client)
        db.session.commit()

    client = Client.query.first()

    assert Client.query.count() == 1
    assert client.login == 'login1'
    assert client.email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)

    with pytest.raises(IntegrityError):
        client_err_1 = Client(login='login1', email='client1@client',
                              password='pass1')

        db.session.add(client_err_1)
        db.session.commit()


def test_update_row(app_test, create_client_one):
    """Обновление записи в БД."""
    with app_test.app_context():
        new_client = create_client_one

        db.session.add(new_client)
        db.session.commit()

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login1'
    assert Client.query.first().email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)

    with app_test.app_context():
        client = Client.query.first()
        client.login = 'login2'
        client.email = 'client2@client'
        client.password = bcrypt.hash('pass2')

        db.session.commit()

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login2'
    assert Client.query.first().email == 'client2@client'
    assert bcrypt.verify('pass2', Client.query.first().password)


def test_delete_row(app_test, create_client_one, create_client_two):
    """Удаление записи в БД."""
    with app_test.app_context():
        new_client_1 = create_client_one
        new_client_2 = create_client_two

        db.session.add_all([new_client_1, new_client_2])
        db.session.commit()

    assert Client.query.count() == 2
    assert Client.query.first().login == 'login1'
    assert Client.query.first().email == 'client1@client'
    assert bcrypt.verify('pass1', Client.query.first().password)

    with app_test.app_context():
        Client.query.filter(Client.id == 1).delete()
        db.session.commit()

    assert Client.query.count() == 1
    assert Client.query.first().login == 'login2'
    assert Client.query.first().email == 'client2@client'
    assert bcrypt.verify('pass2', Client.query.first().password)
