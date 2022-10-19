from sqlalchemy import desc

from app.vote.model import Vote
from .settings import MAX_ANSWER_ON_VOTE, MAX_VOTES_CLIENT


def check_access_vote(client_id: int, vote_id: int) -> bool:
    """Проверка доступа у пользователя к опросу.
        :param client_id -- id пользователя.
        :type client_id: int
        :param vote_id -- id опроса.
        :type vote_id: int
        :return True если есть право доступа, иначе False.
    """
    vote = Vote.query.filter(Vote.client_id == client_id,
                             Vote.id == vote_id).first()
    return True if vote else False


def check_max_answer_vote(current_answer: int) -> bool:
    """Проверка количества ответов на опрос.
        :param current_answer -- текущее количество ответов.
        :type current_answer: int
    """
    return True if current_answer < MAX_ANSWER_ON_VOTE else False


def check_max_votes_client(current_votes: int) -> bool:
    """Проверка количества опросов созданных клиентом.
        :param current_votes -- текущее количество опросов.
        :type current_votes: int
    """
    return True if current_votes < MAX_VOTES_CLIENT else False


def get_votes_on_status(client_id: int, status: str) -> list:
    """Возвращает список опросов клиента, со статусом status(параметр).
        :param client_id -- id клиента.
        :type client_id: int
        :param status -- статус, который надо найти
                        ('waiting','started','finished')
        :type status: str
        :return votes_client -- список опросов клиента.
        :rtype votes_client: list
    """
    try:
        votes_client = Vote.query.filter(Vote.client_id == client_id).\
            filter(Vote.status == status).order_by(desc(Vote.create)).all()

    except Exception as e:
        raise Exception(f'{e}')

    return votes_client


def get_votes_count(client_id: int, status: str) -> int:
    """Возвращает количество опросов клиента, со статусом status(параметр).
        :param client_id -- id клиента.
        :type client_id: int
        :param status -- статус, который надо найти
                        ('waiting','started','finished')
        :type status: str
        :return votes_count -- список опросов клиента.
        :rtype votes_count: int
    """
    try:
        votes_count = Vote.query.filter(Vote.status == status,
                                        Vote.client_id == client_id).count()

    except Exception as e:
        raise Exception(f'{e}')

    return votes_count


def get_result_vote(vote_id: int) -> list:
    """Возвращает словарь со статистикой по опросу.
       :param vote_id -- id опроса.
       :type vote_id: int
       :return statistic -- список из словарей содержащий ответ, кол-во
                            проголосовавших за ответ и процентное соотношение
                            в опросе.
       :rtype  statistic: list
    """
    statistic = list()
    try:
        vote = Vote.query.get(vote_id)
        if not vote:
            raise Exception("Нет опроса чтобы получить результат")

        total = 0
        for answer in Vote.query.get(vote_id).rs_answer:
            total += answer.number_votes

        statistic.append({'total': total})

        for answer in vote.rs_answer:
            temp_dict = dict()
            temp_dict['answer'] = answer.answer
            temp_dict['number_votes'] = answer.number_votes
            temp_dict['percent'] = round(answer.number_votes * 100 / total, 1)

            statistic.append(temp_dict)

    except Exception as e:
        raise Exception(f'{e}')

    return statistic
