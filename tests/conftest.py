import pytest
from flask_jwt_extended import JWTManager

from app import create_app
from config import ConfigTest
from app.models import db
from app.client.model import Client


# ------------------------------ main ------------------------------------------
@pytest.fixture
def app_test():
    app = create_app(config_class=ConfigTest)

    JWTManager(app)

    with app.app_context():
        db.create_all()

        yield app

        db.drop_all()


# ------------------------------ main ------------------------------------------
# ------------------------------ client start ----------------------------------
@pytest.fixture
def create_client_one():
    return Client(login='login1', email='client1@client', password='pass1')


@pytest.fixture
def create_client_two():
    return Client(login='login2', email='client2@client', password='pass2')


# ------------------------------ client end ------------------------------------
