FROM python:3.4

RUN pip install pipenv==8.2.7 \
  && pip install awscli==1.11.174
RUN apt update && apt install -y libsnappy-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV AWS_DEFAULT_REGION eu-west-1

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system

EXPOSE 5000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

COPY . /usr/src/app
