FROM onsdigital/docker-aws-apache-wsgi:python-3.4.2-onbuild

# Install branched Python Cryptography to fix Apache issue
# TO BE REMOVED ONCE OFFICIAL PACKAGE (1.8?) RELEASED
RUN yum install -y git && \
    pip install -e git+https://github.com/reaperhulk/cryptography.git@password-cb#egg=cryptography

# Compile frontend
RUN yarn compile

# Because eq-survey-runner creates 'eq.log' in the current directory
# it needs write permission as the apache user
RUN chown apache:apache .
