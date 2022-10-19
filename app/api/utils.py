from flask_jwt_extended import decode_token

from app.client.model import Client


class AccessClient:
    """Проверяет headers запроса и возвращает данные(объект) клиента если у него
        есть доступ.

        Методы:
            check() -- Получает заголовок и раскодирует токен.
    """
    def check(self, headers: dict) -> Client:
        """Получает заголовок и раскодирует токен и возвращает
            данные(объект) клиента.
        """
        self._headers = headers

        if not self._headers:
            raise Exception('Отсутствует headers в запросе')

        if not self._headers.get('Authorization'):
            raise Exception('Отсутствует token в запросе')

        self._token = self._get_token_from_header()

        return Client.query.filter_by(email=self._decode_token_api()).first()

    def _get_token_from_header(self) -> str:
        """Возвращает токен из заголовка(headers) если он есть.
            :param headers -- данные заголовка запроса.
            :type headers: dict
        """
        if not self._headers.get('Authorization'):
            raise Exception('Отсутствует token в запросе')

        return self._headers['Authorization'].split(' ')[-1]

    def _decode_token_api(self):
        """Проверяет действительность токена и возвращает раскодированное
            значение вшитое в токен.
            :param token_api -- токен API для проверки.
            :type token_api: str
        """
        try:
            return decode_token(self._token)['sub']

        except Exception:
            raise Exception('Неверный токен')
