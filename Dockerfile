FROM python:3.8.10-slim

COPY requirements.txt /requirements/requirements.txt
RUN pip install -U pip && pip install -r requirements/requirements.txt

COPY . /app
WORKDIR /app

RUN useradd demo
USER demo

EXPOSE 8080

ENTRYPOINT ["bash", "/app/bin/run.sh"]