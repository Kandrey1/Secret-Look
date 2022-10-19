import pytest
from flask_jwt_extended import JWTManager

from app import create_app
from app.vote.model import Vote, VoteAnswer
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

        db.session.close()
        db.drop_all()


@pytest.fixture
def client_test(app_test):
    from app.api.blueprint import api_bp
    app_test.register_blueprint(api_bp, url_prefix='/api')
    return app_test.test_client()


# ------------------------------ main ------------------------------------------
# ------------------------------ client start ----------------------------------
@pytest.fixture
def create_client_one():
    return Client(login='login1', email='client1@client', password='pass1')


@pytest.fixture
def create_client_two():
    return Client(login='login2', email='client2@client', password='pass2')


# ------------------------------ client end ------------------------------------
# ------------------------------ vote start ------------------------------------
@pytest.fixture
def create_vote_one():
    vote = Vote(title='title1',
                date_start='2022-5-10T12:00',
                date_end='2022-5-11T12:00',
                question='question1',
                client_id=1)
    return vote


@pytest.fixture
def create_vote_two():
    vote = Vote(title='title2',
                date_start='2022-6-10T12:00',
                date_end='2022-6-11T12:00',
                question='question2',
                client_id=2)
    return vote


@pytest.fixture
def create_vote_three():
    vote = Vote(title='title3',
                date_start='2022-6-10T12:00',
                date_end='2022-6-11T12:00',
                question='question3',
                client_id=1)
    return vote


@pytest.fixture
def create_vote_answer_one():
    return VoteAnswer(answer='answer1', vote_id=1)


@pytest.fixture
def create_vote_answer_two():
    return VoteAnswer(answer='answer2', vote_id=1)


# ------------------------------ vote end --------------------------------------
# ------------------------------ api start -------------------------------------
# ------------------------------ api end ---------------------------------------
