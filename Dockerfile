FROM python:3.4-onbuild

COPY . /usr/src/app

ENV AWS_DEFAULT_REGION eu-west-1

EXPOSE 5000

# Compile frontend
CMD [ "python", "./application.py", "runserver" ]
