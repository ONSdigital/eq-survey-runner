FROM onsdigital/docker-aws-apache-wsgi:python-3.4.2-onbuild

# Compile frontend
RUN yarn compile
