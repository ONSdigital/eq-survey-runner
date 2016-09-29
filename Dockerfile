FROM ubuntu:15.04

ENV RUNTIME_PACKAGES="python3"
ENV BUILD_PACKAGES="curl build-essential python3-dev postgresql python-psycopg2 libpq-dev ca-certificates libffi-dev libssl-dev"

ADD requirements.txt /code/requirements.txt

# Install all dependencies, cleanup and reinstall python 
# apt's cleanup also uninstalls python, so we have to install again..

RUN apt-get update && apt-get install -y $RUNTIME_PACKAGES $BUILD_PACKAGES \
	&& curl -sS https://bootstrap.pypa.io/get-pip.py | python3

RUN pip3 pip install pip --upgrade
RUN apt-get install -y libevent-dev
RUN pip3 install --no-cache-dir -U -I -r /code/requirements.txt \
	&& apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) \
	&& apt-get install -y $RUNTIME_PACKAGES \
	&& rm -rf /var/lib/apt/lists/*

ADD app /code/app
ADD scripts /code/scripts
ADD application.py /code/application.py
ADD token_generator.py /code/token_generator.py
ADD config.py /code/config.py

WORKDIR /code

ENTRYPOINT ./scripts/startup.sh