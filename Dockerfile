FROM ubuntu:16.04 as builder

RUN apt-get update \
    && apt-get install -y curl git wget locales python-pip make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev apt-transport-https libpq-dev 

RUN locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8

RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.4.2
RUN pyenv global 3.4.2

RUN pip install --upgrade pip setuptools pipenv

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && curl -sL https://deb.nodesource.com/setup_6.x | bash - 

RUN apt-get update \
    && apt-get install -y yarn nodejs

RUN mkdir -p /usr/src/app
COPY . /usr/src/app
RUN ls -al /usr/src/app

WORKDIR /usr/src/app
RUN ./scripts/build.sh

# The .git folder would be in the .dockerignore if we didn't need it for the build script
RUN rm -rf .git

###############################################################################
# Second Stage
###############################################################################

FROM python:3.4

EXPOSE 5000

RUN pip install pipenv==8.2.7 \
  && pip install awscli==1.11.174
RUN apt update && apt install -y libsnappy-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV AWS_DEFAULT_REGION eu-west-1

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --deploy --system

COPY --from=builder /usr/src/app/ /usr/src/app

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
