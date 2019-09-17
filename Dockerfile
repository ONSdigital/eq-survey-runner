FROM python:3.7-stretch as builder

RUN apt-get update \
    && apt-get install -y curl unzip git make build-essential libsnappy-dev

RUN git clone --branch v0.13.0 --depth 1 https://github.com/google/jsonnet.git /tmp/jsonnet \
    && make -C /tmp/jsonnet \
    && cp /tmp/jsonnet/jsonnet /usr/local/bin

WORKDIR /runner

COPY . /runner

RUN mkdir -p /runner/data/en
RUN pip install pipenv==2018.11.26
RUN pipenv install --deploy
ENV EQ_RUNNER_BASE_DIRECTORY=/runner
RUN pipenv run ./scripts/build.sh

###############################################################################
# Second Stage
###############################################################################

FROM python:3.7-slim-stretch

EXPOSE 5000

RUN apt update && apt install -y git libsnappy-dev build-essential

RUN mkdir -p /runner
WORKDIR /runner

ENV GUNICORN_WORKERS 3
ENV GUNICORN_KEEP_ALIVE 2

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv==2018.11.26

RUN pipenv install --deploy --system

COPY --from=builder /runner /runner

CMD ["sh", "docker-entrypoint.sh"]
