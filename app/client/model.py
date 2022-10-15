import datetime
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from ..models import db, ma


class Client(db.Model):
    """Таблица клиент.
        create -- дата добавления клиента в БД.
        login -- логин клиента.
        email -- почта клиента.
        password -- пароль клиента.

        Методы:
            get_hash_pass -- Возвращает преобразованный hash функцией
                         пароль(строку).
            get_token -- Возвращает токен клиента.
            authenticate -- Проверяет есть ли пользователь с email и
                            password в БД.
    """
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    create = db.Column(db.DateTime, default=datetime.datetime.today())
    login = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(350), nullable=False)
    # todo возможно добавить IP с которого идет регистрация аккаунта

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password = self.get_hash_pass(password=password)

    def __repr__(self):
        return f"<{self.ip_reg} : {self.login} - {self.email}>"

    @classmethod
    def get_hash_pass(cls, password: str) -> str:
        """Возвращает преобразованный hash функцией пароль(строку)."""
        return bcrypt.hash(password)

    def get_token(self, expire_time: int = 24) -> str:
        """Возвращает токен клиента.
            :param expire_time -- время действие токена в часах.
            :type expire_time: int
            :return token -- токен авторизованного пользователя.
            :rtype token: str
        """
        expire_delta = datetime.timedelta(expire_time)
        token = create_access_token(identity=self.id,
                                    expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email: str, password: str) -> object:
        """Проверяет есть ли пользователь с email и password в БД.
            :param email -- email, который необходимо проверить.
            :type email: str
            :param password -- пароль, который необходимо проверить.
            :type password: str
            :return client -- Объект client(содержащий информацию
                              пользователя) из БД.
            :rtype client: object
        """
        client = cls.query.filter(cls.email == email).first()
        if not client or not bcrypt.verify(password, client.password):
            raise Exception('Неправильный email или пароль')

        return client


class ClientSchema(ma.Schema):
    class Meta:
        model = Client
        fields = ('id', 'create', 'login', 'email')
