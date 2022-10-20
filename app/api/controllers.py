from flask import request, jsonify
from flask_restful import Resource

from .utils import AccessClient
from app.vote.model import Vote, VoteAnswer, VoteSchema
from app.utils import Database
from ..vote.settings import MAX_ANSWER_ON_VOTE
from ..vote.utils import check_max_answer_vote, check_max_votes_client, \
    check_access_vote


class AllVoteClient(Resource):
    """Содержит два метода:
       post -- Добавляет новой опрос с вариантами ответа.
       get -- Возвращает список всех опросов клиента.
    """
    def post(self):
        """Добавляет новой опрос с вариантами ответа.
            Данные для добавления передаются в формате json
            {"title": "", "question": "", "date_start": "", "date_end": "",
            "answers":["answer1", "answer2",...]}
            Дата в формате строки '%Y-%m-%dT%H:%M' (прим. '2018-06-29T08:15')
        """
        try:
            client = AccessClient().check(headers=request.headers)

            datas = request.get_json()
            # todo проверка корректности данных

            if not check_max_votes_client(current_votes=len(client.rs_vote)):
                raise Exception('Вы достигли лимита создания опросов')

            if not check_max_answer_vote(current_answer=len(datas["answers"])):
                raise Exception(f'Вы можете добавить максимум='
                                f'{MAX_ANSWER_ON_VOTE} ответов.')

            vote = Vote(title=datas["title"],
                        question=datas["question"],
                        date_start=datas["date_end"],
                        date_end=datas["date_start"],
                        client_id=client.id)
            Database.save(vote)

            for ans in datas["answers"]:
                answer = VoteAnswer(answer=ans, vote_id=vote.id)
                Database.save(answer)

        except Exception as e:
            return {'Error': f'{e}'}

        return jsonify({f'{datas["title"]}': 'Add'})

    def get(self):
        """Возвращает список всех опросов клиента."""
        try:
            client = AccessClient().check(headers=request.headers)

            votes = list()

            for v in client.rs_vote:
                votes.append(VoteSchema().dump(v))

        except Exception as e:
            return {'Error': f'{e}'}

        return jsonify({'Опросы': votes})


class VoteClient(Resource):
    """Содержит два метода:
        get -- Возвращает подробную информацию по опросу.
        delete -- Удаляет опрос, если он в статусе 'waiting'(не запущен).
    """
    def get(self, vote_id: int):
        """Возвращает подробную информацию по опросу с ответами и
            количеством проголосовавших.
        """
        try:
            client = AccessClient().check(headers=request.headers)

            if not check_access_vote(client_id=client.id, vote_id=vote_id):
                raise Exception('Запрошенный опрос не существует')

            vote = Vote.query.filter(Vote.client_id == client.id,
                                     Vote.id == vote_id).first()
            votes = VoteSchema().dump(vote)

            answers = [{a.answer: a.number_votes} for a in vote.rs_answer]

            votes.update({"answers": answers})

        except Exception as e:
            return {'Error': f'{e}'}

        return jsonify(votes)

    def delete(self, vote_id: int):
        """Удаляет опрос, если он в статусе 'waiting'(не запущен).
            Дополнительно надо передать в json {"mode": "delete"}
        """
        try:
            client = AccessClient().check(headers=request.headers)

            datas = request.get_json()

            if not datas['mode'] == 'delete':
                raise Exception('Неверный запрос удаления')

            if not check_access_vote(client_id=client.id, vote_id=vote_id):
                raise Exception('Запрошенный опрос не существует')

            Database.dell(table=Vote, delete_id=vote_id)

        except Exception as e:
            return {'Error': f'{e}'}

        return jsonify()
