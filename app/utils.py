import datetime

from sqlalchemy.exc import IntegrityError

from .client.model import Client
from .models import db


class Database:
    """Методы для работы с БД.
        save() -- сохраняет запись в БД.
        up() -- обновляет данные записи в БД.
        dell() -- удаляет запись из БД.
    """
    @staticmethod
    def save(row: object) -> None:
        """Сохраняет запись в БД.
            :param row -- строка, которую надо сохранить.
            :type row: object
        """
        try:
            db.session.add(row)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            raise Exception("Такой email уже есть.")

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Запись не сохранена {e}")

    @staticmethod
    def dell(table: db.Model, delete_id: int) -> None:
        """Удаляет запись из БД.
            :param table -- таблица из которой требуется удалить запись.
            :type table: db.Model
            :param delete_id -- id записи, которую требуется удалить.
            :type  delete_id: int
        """
        try:
            row = db.session.query(table).filter(table.id == delete_id).first()
            db.session.delete(row)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Ошибка при удалении записи из БД{e}")

    @staticmethod
    def up(table: db.Model, update_id: int, data_update: dict) -> None:
        """Обновляет данные записи клиента в БД.
            :param table -- таблица в которой необходимо обновить данные.
            :type table: db.Model
            :param update_id -- id записи обновления.
            :type update_id: int
            :param data_update - словарь с данными для обновления формата
                                {"": "", "": ""}
            :type data_update: dict
        """
        try:
            row = table.query.get(update_id)

            if not row:
                raise Exception("UP.Нет такой записи")

            for key, val in data_update.items():
                if val:
                    if key == 'password':
                        setattr(row, key, Client.get_hash_pass(val))
                    elif key in ['date_start', 'date_end']:
                        setattr(row, key, Converter.str_in_datetime(val))
                    else:
                        setattr(row, key, val)

            db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise Exception(f"Ошибка при обновлении записи в БД {ex}")


class Converter:
    """Содержит методы преобразования данных.
        str_in_datetime() -- Преобразует строку в datetime.
        datetime_in_str() -- Преобразует datetime в строку.
    """
    __FORMAT_DATE = '%Y-%m-%dT%H:%M'

    @staticmethod
    def str_in_datetime(date_time_str: str) -> datetime:
        """Преобразует дату date_time_str в формате строки в объект datetime.
           Дата в формате строки '%Y-%m-%dT%H:%M' (прим. '2018-06-29T08:15')
        """
        return datetime.datetime.strptime(date_time_str,
                                          Converter.__FORMAT_DATE)

    @staticmethod
    def datetime_in_str(date_time_obj: datetime) -> str:
        """Преобразует date_time_obj объект datetime в строку.
           Формат строки '%Y-%m-%dT%H:%M' (прим. '2018-06-29T08:15')
        """
        return date_time_obj.strftime(Converter.__FORMAT_DATE)
