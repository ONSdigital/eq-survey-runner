FROM ubuntu:15.04

ENV RUNTIME_PACKAGES="python3 postgresql python-psycopg2"
ENV BUILD_PACKAGES="curl build-essential python3-dev libpq-dev ca-certificates libffi-dev libssl-dev"

WORKDIR /code

EXPOSE 5000

RUN apt-get update && apt-get install -y $RUNTIME_PACKAGES $BUILD_PACKAGES \
	&& curl -sS https://bootstrap.pypa.io/get-pip.py | python3 \
	&& curl -sL https://deb.nodesource.com/setup_5.x | bash -

RUN apt-get install -y nodejs
RUN npm install --global gulp-cli

ADD requirements.txt /code/requirements.txt

RUN pip3 install -U -I -r /code/requirements.txt

ADD . /code

RUN npm install && npm run compile

ENTRYPOINT python3 application.py runserver
