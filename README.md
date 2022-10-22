# SecretLook
Web приложение "SecretLook" предназначено для проведения опросов и анонимного анкетирования.
Позволяет зарегистрированному клиенту в личном кабинете создать опрос, анкеты и разместить
ссылку на них у себя. Клиент может получать статистику по итогам опроса и анкетирования.
(front реализован для оценки функциональности)

## Технологий
 - ЯП: Python 
 - Фреймворк: Flask 
 - ORM: SQLAlchemy
 - ДБ: Postgres
 - Celery + Redis

## Реализовано
 - Регистрация клиента и авторизация с помощью Jwt Token.
 - Личный кабинет. CRUD данных клиента.
 - REST API сервис для клиентов. Для доступа к API необходим токен(можно получить в личном кабинете).
 - Автоматический запуск и завершение опросов.

## Установка
Выполнить следующие команды:

Клонировать репозиторий: `git clone https://github.com/Kandrey1/https://github.com/Kandrey1/Secret-Look.git`

Перейти в директорию: `cd Secret-Look`

Создать виртуальное окружение командой: `python -m venv venv`

Установить пакеты: `pip install -r requirements.txt`

Создать файл .env (образец .env_sample).
Создать файл .flaskenv (образец .flaskenv_sample).

### Запуск

#### Без Docker
(У Вас должны быть установлены Redis (localhost:6379) и Postgres(localhost:5432), 
если они на других портах необходимо будет указать их в конфигурациях)

Установить в файле .env параметры: 
 - POSTGRES_HOSTNAME=localhost
 - REDIS_HOST=localhost

Находясь в корне проекта выполнить: 
 - worker `celery -A celeryd worker --loglevel=INFO --concurrency 4 -P eventlet  --purge`
 - beat `celery -A celeryd beat --loglevel=INFO`
 - flower (необязательно) `celery -A celeryd flower --loglevel=info`

#### Используя Docker

Установить в файле .env параметры: 
 - POSTGRES_HOSTNAME=postgres
 - REDIS_HOST=redis

 - Находясь в корне проекта выполнить: 

`docker-compose up --build -d`

При первом запуске потребуется время создание БД.(в это время приложение может выдавать ошибку)

Автоматически устанавливается pgAdmin по адресу `http://localhost:5050/browser/` 


## Тестирование

Для тестирования необходимо уставить pytest `pip install pytest`

Выполнить команды для запуска тестирования `pytest tests`

В Postgres должна быть  БД с именем "test_secretlook".