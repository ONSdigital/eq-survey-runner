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


RUN git clone --branch v0.12.1 --depth 1 https://github.com/google/jsonnet.git /tmp/jsonnet \
    && make -C /tmp/jsonnet \
    && cp /tmp/jsonnet/jsonnet /usr/local/bin

WORKDIR /runner

COPY app/assets /runner/app/assets
COPY package.json /runner/
COPY yarn.lock /runner/
RUN yarn install

COPY gulpfile.babel.js /runner/
COPY gulp/* /runner/gulp/
COPY .babelrc .eslint* .stylelintrc .tern-project .yarnrc /runner/
RUN yarn compile

COPY scripts/build_schemas.sh /runner/
COPY data-source /runner/data-source
RUN mkdir -p /runner/data/en
RUN ./build_schemas.sh

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

COPY . /runner
COPY --from=builder /runner/static /runner/static
COPY --from=builder /runner/data/en/* /runner/data/en/

CMD ["sh", "docker-entrypoint.sh"]
