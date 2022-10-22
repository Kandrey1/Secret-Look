import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class ConfigDevelopment(object):
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    DB_URL = 'postgresql+psycopg2://{user}:{psw}@{url}/{db}'.format(
        user=os.environ.get('POSTGRES_USER'),
        psw=os.environ.get('POSTGRES_PASSWORD'),
        url=f"{os.environ.get('POSTGRES_HOSTNAME')}:"
            f"{os.environ.get('POSTGRES_PORT')}",
        db=os.environ.get('POSTGRES_DB'))

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    PROPAGATE_EXCEPTIONS = True

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')


class ConfigTest(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_URL = 'postgresql+psycopg2://{user}:{psw}@{url}/{db}'.format(
        user=os.environ.get('POSTGRES_USER'),
        psw=os.environ.get('POSTGRES_PASSWORD'),
        url=f"{os.environ.get('POSTGRES_HOSTNAME')}:"
            f"{os.environ.get('POSTGRES_PORT')}",
        db=os.environ.get('POSTGRES_DB_TEST'))
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
