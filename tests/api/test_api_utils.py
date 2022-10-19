from app.api.utils import AccessClient
from app.client.model import Client
from app.models import db


# ----------------- Vote start -------------------------------------------------
def test_api_utils_access_client(app_test, client_test, create_client_one):
    """Проверяет headers запроса и возвращает данные(объект) клиента если у него
        есть доступ."""
    with app_test.app_context():
        client1 = create_client_one
        db.session.add(client1)
        db.session.commit()

        token_api = client1.get_token_api()

    assert Client.query.count() == 1

    headers = {
        "Authorization": f"Bearer {token_api}",
        "Accept": "*/*"
    }

    client = AccessClient().check(headers=headers)

    assert Client.query.count() == 1
    assert client.id == client1.id
    assert client.email == client1.email
