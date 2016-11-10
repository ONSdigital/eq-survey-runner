FROM ubuntu:14.04

ENV RUNTIME_PACKAGES="python3 postgresql python-psycopg2"
ENV BUILD_PACKAGES="curl build-essential python3-dev libpq-dev ca-certificates libffi-dev libssl-dev git"

WORKDIR /code

EXPOSE 5000

RUN apt-key adv --keyserver pgp.mit.edu --recv D101F7899D41F3C3

RUN echo "deb http://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get update && apt-get install -y $RUNTIME_PACKAGES $BUILD_PACKAGES \
	&& curl -sS https://bootstrap.pypa.io/get-pip.py | python3 \
	&& curl -sL https://deb.nodesource.com/setup_6.x | bash -

RUN apt-get install -y nodejs yarn
RUN yarn global add gulp-cli

ADD requirements.txt /code/requirements.txt
ADD package.json /code/package.json
ADD app/assets /code/app/assets

RUN pip3 install -U -I -r /code/requirements.txt

ADD . /code

RUN yarn compile

ENTRYPOINT python3 application.py runserver
