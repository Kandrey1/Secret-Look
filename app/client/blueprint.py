from flask import Blueprint, render_template, flash, redirect, \
    url_for, make_response, session
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies, \
    jwt_required, get_jwt_identity

from .forms import RegisterForm, AuthForm
from .model import Client
from app.utils import Database
from ..vote.utils import get_votes_count

client_bp = Blueprint('client', __name__)


@client_bp.route("/register", methods=['GET', 'POST'])
def register():
    """Регистрация нового клиента."""
    form = RegisterForm()
    context = dict()
    context['title'] = 'Регистрация'
    try:
        if form.validate_on_submit():
            new_client = Client(login=form.login.data,
                                email=form.email.data,
                                password=form.password.data)

            Database.save(row=new_client)

            token = new_client.get_token()

            redirect_profile = make_response(redirect(
                url_for('client.profile')))
            set_access_cookies(redirect_profile, token)

            session['user_login'] = new_client.login

            return redirect_profile

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("client/register.html", form=form, context=context)


@client_bp.route("/auth", methods=['GET', 'POST'])
def auth():
    """Авторизация клиента."""
    form = AuthForm()
    context = dict()
    context['title'] = 'Авторизация'
    try:

        if form.validate_on_submit():
            check_client = Client.authenticate(email=form.email.data,
                                               password=form.password.data)
            if check_client:
                token = check_client.get_token()
                redirect_profile = make_response(redirect(
                    url_for('client.profile')))
                set_access_cookies(redirect_profile, token)

                session['user_login'] = check_client.login

                return redirect_profile

    except Exception as e:
        flash(f'Error: <{e}>')

    return render_template("client/auth.html", form=form, context=context)


@client_bp.route("/logout/", methods=['GET'])
@jwt_required()
def logout():
    """Logout."""
    session.pop('user_login', None)
    redirect_index = make_response(redirect(url_for('index')))
    unset_jwt_cookies(redirect_index)
    return redirect_index


@client_bp.route("/profile", methods=['GET', 'POST'])
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
