FROM ubuntu:18.04 as builder

RUN apt-get update \
    && apt-get install -y curl git locales make build-essential

RUN locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash -

RUN apt-get update \
    && apt-get install -y yarn nodejs

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN yarn compile

# We don't want node_modules to be copied to the runtime image
RUN rm -rf node_modules
###############################################################################
# Second Stage
###############################################################################

FROM python:3.7-slim-stretch

EXPOSE 5000

RUN apt update && apt install -y libsnappy-dev build-essential

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV GUNICORN_WORKERS 3

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv==2018.11.26

RUN pipenv install --deploy --system

COPY --from=builder /usr/src/app/ /usr/src/app

CMD ["sh", "docker-entrypoint.sh"]
