FROM ubuntu:18.04 as builder

RUN apt-get update \
    && apt-get install -y curl unzip git make build-essential

RUN git clone --branch v0.12.1 --depth 1 https://github.com/google/jsonnet.git /tmp/jsonnet \
    && make -C /tmp/jsonnet \
    && cp /tmp/jsonnet/jsonnet /usr/local/bin

WORKDIR /runner

COPY . /runner
RUN ./scripts/load_templates.sh

RUN mkdir -p /runner/data/en
RUN ./scripts/build_schemas.sh

###############################################################################
# Second Stage
###############################################################################

FROM python:3.7-slim-stretch

EXPOSE 5000

RUN apt update && apt install -y libsnappy-dev build-essential

RUN mkdir -p /runner
WORKDIR /runner

ENV GUNICORN_WORKERS 3

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv==2018.11.26

RUN pipenv install --deploy --system

COPY --from=builder /runner /runner

CMD ["sh", "docker-entrypoint.sh"]
