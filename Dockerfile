FROM python:3.7

RUN pip install pipenv==2018.7.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV AWS_DEFAULT_REGION eu-west-1

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system

EXPOSE 5000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

COPY . /usr/src/app
