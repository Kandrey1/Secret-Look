from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.hash import bcrypt

from app.utils import Database
from app.client.model import Client
from app.profile.forms import ChangePassForm, DeleteAccountForm
from app.vote.utils import get_votes_count


profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/", methods=['GET', 'POST'])
@jwt_required()
def profile():
    """Личный кабинет клиента."""
    context = dict()
    context['title'] = 'Личный кабинет'
    try:
        current_client = get_jwt_identity()

        context['stared_count'] = get_votes_count(client_id=current_client,
                                                  status='started')
        context['waiting_count'] = get_votes_count(client_id=current_client,
                                                   status='waiting')
        context['finished_count'] = get_votes_count(client_id=current_client,
                                                    status='finished')

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("profile/profile.html", context=context)


@profile_bp.route("/settings", methods=['GET', 'POST'])
@jwt_required()
def settings():
    """Настройки личного кабинета клиента."""
    context = dict()
    context['title'] = 'Настройки'
    try:
        client = Client.query.get(get_jwt_identity())
        context['client'] = client
        context['token_api'] = request.args.get('token_api')

        if request.method == "POST":
            if "get_token_api" in request.form:
                token = client.get_token_api()
                return redirect(url_for('profile.settings', token_api=token))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("profile/settings.html", context=context)


@profile_bp.route("/change_pass", methods=['GET', 'POST'])
@jwt_required()
def change_pass():
    """Изменение пароля клиента."""
    form = ChangePassForm()
    context = dict()
    context['title'] = 'Смена пароля'
    try:
        if form.validate_on_submit():
            client = Client.query.get(get_jwt_identity())
            if not bcrypt.verify(form.old_pass.data, client.password):
                raise Exception('Неверный старый пароль')

            Database.up(table=Client, update_id=client.id,
                        data_update={'password': form.password.data})

            flash('Пароль успешно изменен')

            return redirect(url_for('profile.settings'))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("profile/change_pass.html", context=context,
                           form=form)


@profile_bp.route("/delete_account", methods=['GET', 'POST'])
@jwt_required()
def delete_account():
    """Удаление аккаунта."""
    form = DeleteAccountForm()
    context = dict()
    context['title'] = 'Удаление аккаунта'
    try:
        if form.validate_on_submit():
            client = Client.query.get(get_jwt_identity())

            if not bcrypt.verify(form.pass_for_dell.data, client.password):
                raise Exception('Неверный пароль')

            Database.dell(table=Client, delete_id=client.id)

            return redirect(url_for('client.logout'))

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("profile/delete_account.html", context=context,
                           form=form)
