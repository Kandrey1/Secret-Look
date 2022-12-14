from flask import render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_swagger_ui import get_swaggerui_blueprint

from app import create_app
from app.api.blueprint import api_bp
from app.client.blueprint import client_bp
from app.profile.blueprint_profile import profile_bp
from app.models import db
from app.vote.blueprint import vote_bp
from cache import cache


app = create_app()

jwt = JWTManager(app)

cache.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


SWAGGER_URL = '/docs/api'
API_URL = '/static/swagger/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'API Secret Look'
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(client_bp, url_prefix='/client')
app.register_blueprint(profile_bp, url_prefix='/client/profile')
app.register_blueprint(vote_bp, url_prefix='/vote')


@app.route("/")
def index():
    """Главная страница приложения."""
    context = dict()
    context['title'] = "Secret Look"
    return render_template("index.html", context=context)


@app.route("/about/api/")
def about_api():
    """Страница с описанием API сервиса."""
    context = dict()
    context['title'] = "API"
    return render_template("api/info.html", context=context)


@app.route("/survey")
def survey():
    """Публичные анкеты."""
    context = dict()
    context['title'] = "Survey"
    return render_template("survey/public.html", context=context)


@app.errorhandler(404)
def page_not_found(error):
    """Ошибка 404."""
    context = dict()
    context['title'] = "Страница не найдена"
    return render_template('page404.html', context=context), 404


@app.errorhandler(NoAuthorizationError)
def handle_auth_error(error):
    """Ошибка 401. При попытке доступа к странице без авторизации."""
    context = dict()
    context['title'] = "Доступ запрещен"
    return render_template('page401.html', context=context), 401
