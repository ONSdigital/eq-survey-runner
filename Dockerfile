FROM onsdigital/flask-crypto-queue

ADD . /code

RUN mkdir -p /app/logs

RUN pip3 install --no-cache-dir -U -I -r /code/requirements.txt

ENTRYPOINT /code/scripts/startup.sh