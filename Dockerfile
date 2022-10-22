FROM python:3.9-slim
WORKDIR ./app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP='main.py' FLASK_DEBUG=TRUE
CMD ["flask", "run"]