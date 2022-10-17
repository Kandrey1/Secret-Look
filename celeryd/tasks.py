import datetime

from app import create_app
from app.vote.model import Vote
from celeryd.celery import clr

app = create_app()


@clr.task
def check_vote_which_be_running():
    """Проверяет, есть ли опросы, которые должны были быть
        запущены по времени, но по факту не запущены.
    """
    try:
        time_now = datetime.datetime.today()

        with app.app_context():
            not_run_vote = Vote.query.filter(Vote.date_start <= time_now,
                                             Vote.status == 'waiting').all()

            for vote in not_run_vote:
                started_vote.apply_async((vote.id,), eta=None)

    except Exception:
        return False

    return True


@clr.task
def check_vote_which_be_finished():
    """Проверяет, есть ли опросы, которые надо завершить ближайшее время.
    """
    try:
        time_now = datetime.datetime.today()
        with app.app_context():
            finish_vote = Vote.query.filter(Vote.date_end <= time_now,
                                            Vote.status == 'started').all()

        for vote in finish_vote:
            finished_vote.apply_async((vote.id, ), eta=None)

    except Exception:
        return False

    return True


@clr.task(bind=True, max_retries=2, soft_time_limit=30, time_limit=40)
def started_vote(self, vote_id: int) -> bool:
    """Запускает опрос.
        Возвращает True в случае успеха, иначе False.
    """
    try:
        with app.app_context():
            vote = Vote.query.get(vote_id)
            vote.set_status_started()

    except Exception:
        return False

    return True


@clr.task(bind=True, max_retries=2, soft_time_limit=30, time_limit=40)
def finished_vote(self, vote_id: int) -> bool:
    """Завершает опрос.
        Возвращает True в случае успеха, иначе False.
    """
    try:
        with app.app_context():
            vote = Vote.query.get(vote_id)
            vote.set_status_finished()

    except Exception:
        return False

    return True
