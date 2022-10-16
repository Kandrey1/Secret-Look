import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigDevelopment(object):
    DEBUG = True
    TRAP_HTTP_EXCEPTIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY_DEVELOPMENT')

    # todo заменить на Postgres после формирования структуры приложения
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(basedir, 'database/db.sqlite3')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    PROPAGATE_EXCEPTIONS = True

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300


class ConfigTest(object):
    DEBUG = True
    SECRET_KEY = 'fgkjlhweriuywq324h3g24hjg32j4k124g32l;gg'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(basedir, 'tests/db_test.sqlite3')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
