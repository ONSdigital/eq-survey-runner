FROM python:3.4-onbuild

COPY . /usr/src/app

ENV AWS_DEFAULT_REGION eu-west-1

EXPOSE 5000

CMD [ "gunicorn", "-b 0.0.0.0:5000", "application:application" ]
