FROM python:3.4-onbuild

ENV AWS_DEFAULT_REGION eu-west-1

EXPOSE 5000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
