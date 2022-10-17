import datetime

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import Database, Converter
from cache import cache
from .model import Vote, VoteAnswer
from .utils import get_votes_on_status, check_access_vote, \
    get_result_vote, check_max_answer_vote, check_max_votes_client
from .forms import VoteForm
from ..models import db
from .settings import MAX_VOTE_PER_PAGE

vote_bp = Blueprint('vote', __name__)


@vote_bp.route("/active_vote/<int:page>", methods=['GET', 'POST'])
def active_vote(page=1):
    """Активные опросы."""
    context = dict()
    context['title'] = 'Активные опросы'
    try:
        if request.method == "GET":
            per_page = MAX_VOTE_PER_PAGE

            vote = Vote.query.filter(Vote.status == 'started')

            context['votes'] = vote.order_by(Vote.date_start.desc()).\
                paginate(page, per_page, error_out=False)

            context['votes_count'] = vote.count()

            context['page'] = page
            context['max_page'] = vote.count() // per_page + 1

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/active_vote.html", context=context)


@vote_bp.route("/show/<string:vote_url>", methods=['GET', 'POST'])
def show_vote(vote_url: str):
    """Страница запущенного опроса."""
    context = dict()
    voted = None
    try:
        if request.method == "GET":
            vote_show = Vote.query.get(Vote.get_id_from_short_url(vote_url))

            context['title'] = f'Опрос: {vote_show.title}'
            context['vote'] = vote_show

            voted = request.args.get('voted')
            if voted == 'yes':
                context['result'] = get_result_vote(vote_show.id)

            return render_template("vote/show_vote.html", context=context)

        if request.method == "POST":
            if "case__answer" in request.form:
                case_answer = request.form.get('answer_case', type=int)

                if case_answer:
                    VoteAnswer.update_number(id_update=case_answer)
                    voted = 'yes'
                else:
                    flash('Необходимо выбрать вариант ответа.')
                return redirect(url_for('vote.show_vote', vote_url=vote_url,
                                        voted=voted))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/show_vote.html", context=context)


@vote_bp.route("/", methods=['GET', 'POST'])
@jwt_required()
def votes():
    """Главная страница опросов."""
    context = dict()
    context['title'] = 'Опросы'
    try:
        if request.method == "GET":
            current_client = get_jwt_identity()

            context['started_votes'] = get_votes_on_status(
                client_id=current_client, status='started')
            context['waiting_votes'] = get_votes_on_status(
                client_id=current_client, status='waiting')
            context['finished_votes'] = get_votes_on_status(
                client_id=current_client, status='finished')

            return render_template("vote/vote_main.html", context=context)

        if request.method == "POST":
            if "create__vote" in request.form:
                return redirect(url_for('vote.form_new', new_vote=True))

            if "show__statistic" in request.form:
                vote_id_statistic = request.form.get('show__statistic')
                return redirect(url_for('vote.statistic',
                                        vote_id=vote_id_statistic))

            if "redact__vote" in request.form:
                vote_id_redact = request.form.get('redact__vote')
                return redirect(url_for('vote.form_redact',
                                        vote_id_redact=vote_id_redact))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/vote_main.html", context=context)


# todo пересмотреть работу с кэшем.(пока вариант чтобы работало)
@vote_bp.route("/form", methods=['GET', 'POST'])
@jwt_required()
def form_new():
    """Форма создания опроса."""
    form = VoteForm()
    context = dict()
    context['title'] = 'Новый опрос'
    try:
        current_votes = Vote.query.filter_by(
            client_id=get_jwt_identity()).count()

        if not check_max_votes_client(current_votes=current_votes):
            raise Exception('Вы не можете создать больше опросов.')

        if request.args.get('new_vote'):
            cache_clear_new_vote()

        if request.method == "GET" and cache.get('list_answer_vote'):
            context['answers'] = enumerate(cache.get('list_answer_vote'),
                                           start=0)
            context['temp_vote'] = cache.get('list_temp_vote')

            return render_template("vote/form_new.html", context=context,
                                   form=form)

        if form.is_submitted():
            if form.save_vote.data:
                new_vote = Vote(title=form.title.data,
                                question=form.question.data,
                                date_start=Converter.datetime_in_str(
                                    form.date_start.data),
                                date_end=Converter.datetime_in_str(
                                    form.date_end.data),
                                client_id=get_jwt_identity())
                Database.save(row=new_vote)

                if not cache.get('list_answer_vote'):
                    raise Exception("Нет ни одного варианта ответа.")

                cache_save_answers_new_vote(vote_id=new_vote.id)

                flash("Новый опрос создан и добавлен")
                return redirect(url_for('vote.votes'))

            if form.add_answer.data:
                vote_cache = {'title': form.title.data,
                              'question': form.question.data,
                              'date_start': form.date_start.data,
                              'date_end': form.date_end.data}
                cache.set('list_temp_vote', vote_cache)

                if not cache.get('list_answer_vote'):
                    cache.set('list_answer_vote', [form.answer.data])
                else:
                    if check_max_answer_vote(
                            current_answer=len(cache.get('list_answer_vote'))):
                        cache_answers = cache.get('list_answer_vote')
                        cache_answers.append(form.answer.data)
                        cache.set('list_answer_vote', cache_answers)
                    else:
                        flash('Вы уже добавили максимальное кол-во ответов.')

                return redirect(url_for('vote.form_new'))

            if "delete_answer" in request.form:
                number_del = int(request.form.get('delete_answer'))
                cache_delete_answer_new_vote(number_item=number_del)
                return redirect(url_for('vote.form_new'))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/form_new.html", context=context, form=form)


@vote_bp.route("/form/<int:vote_id_redact>", methods=['GET', 'POST'])
@jwt_required()
def form_redact(vote_id_redact: int):
    """Форма редактирования опроса.
        :param vote_id_redact -- id опроса для редактирования.
        :param vote_id_redact: int
    """
    form = VoteForm()
    context = dict()
    context['title'] = 'Редактирование опроса'
    try:
        if not check_access_vote(client_id=get_jwt_identity(),
                                 vote_id=vote_id_redact):
            return render_template("page401.html", context=context)

        if request.method == "GET":
            redact_vote = Vote.query.get(vote_id_redact)

            context['vote_data'] = redact_vote
            context['answers'] = redact_vote.rs_answer
            return render_template("vote/form_redact.html", context=context,
                                   form=form)

        if form.is_submitted():
            if form.save_vote.data:
                vote_update = {'title': form.title.data,
                               'question': form.question.data,
                               'date_start': Converter.datetime_in_str(
                                   form.date_start.data),
                               'date_end': Converter.datetime_in_str(
                                   form.date_end.data)}
                Database.up(table=Vote, update_id=vote_id_redact,
                            data_update=vote_update)
                return redirect(url_for('vote.votes'))

            if form.add_answer.data:
                vote_count = VoteAnswer.query.\
                    filter_by(vote_id=vote_id_redact).count()
                if check_max_answer_vote(current_answer=vote_count):
                    answer = VoteAnswer(answer=form.answer.data,
                                        vote_id=vote_id_redact,
                                        number_votes=0)
                    Database.save(row=answer)
                else:
                    flash('Вы уже добавили максимальное кол-во ответов.')

                return redirect(url_for('vote.form_redact',
                                        vote_id_redact=vote_id_redact))

            if "delete_answer" in request.form:
                number_dell = int(request.form.get('delete_answer'))
                Database.dell(table=VoteAnswer, delete_id=number_dell)
                return redirect(url_for('vote.form_redact',
                                        vote_id_redact=vote_id_redact))

            if "delete__vote" in request.form:
                Database.dell(table=Vote, delete_id=vote_id_redact)
                return redirect(url_for('vote.votes'))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/form_redact.html", context=context)


@vote_bp.route("/statistic/<int:vote_id>", methods=['GET', 'POST'])
@jwt_required()
def statistic(vote_id: int):
    """Статистика по опросу."""
    context = dict()
    context['title'] = 'Статистика опроса'
    try:
        if not check_access_vote(client_id=get_jwt_identity(), vote_id=vote_id):
            return render_template("page401.html", context=context)

        if request.method == "GET":
            context['time_now'] = datetime.datetime.today(). \
                replace(microsecond=0)

            current_vote = Vote.query.get(vote_id)

            context['host'] = 'localhost/'
            context['vote'] = current_vote

            statistic_vote = get_result_vote(vote_id=vote_id)
            context['result_total'] = statistic_vote[0]['total']
            context['result'] = statistic_vote[1:]

        if request.method == "POST":
            if "finished__vote" in request.form:
                vote_finish = Vote.query.filter_by(id=vote_id).first()
                vote_finish.set_client_close_vote()
                return redirect(url_for('vote.votes'))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("vote/statistic.html", context=context)


# ------------------------------ CACHE ----------------------------------------
def cache_clear_new_vote() -> None:
    """Очищает кэш необходимый для создания нового опроса."""
    cache.set('list_answer_vote', None)
    cache.set('list_temp_vote', None)


def cache_save_answers_new_vote(vote_id: int) -> None:
    """Сохраняет данные(ответы на опрос) из кэша в БД.
       :param vote_id -- id опроса
       :param vote_id: int
    """
    try:
        for item in cache.get('list_answer_vote'):
            answer = VoteAnswer(answer=item, vote_id=vote_id, number_votes=0)
            db.session.add(answer)
        db.session.commit()

        cache_clear_new_vote()

    except Exception:
        raise Exception("Ошибка сохранения данных(ответы на опрос) из кэша")


def cache_delete_answer_new_vote(number_item: int) -> None:
    try:
        cache_temp = cache.get('list_answer_vote')
        cache_temp.pop(number_item)
        cache.set('list_answer_vote', cache_temp)
    except Exception:
        raise Exception("Ошибка удаления ответа из кэша")
