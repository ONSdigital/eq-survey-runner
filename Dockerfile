FROM onsdigital/docker-aws-apache-wsgi:python-3.4.2-onbuild

# Install branched Python Cryptography to fix Apache issue
# TO BE REMOVED ONCE OFFICIAL PACKAGE (1.8?) RELEASED
RUN yum install -y git && \
    pip install -e git+https://github.com/ONSdigital/cryptography.git@4a90c254278231d7defeac304a3cfd752e96e786#egg=cryptography

# Compile frontend
RUN yarn compile

# Because eq-survey-runner creates 'eq.log' in the current directory
# it needs write permission as the apache user
RUN chown apache:apache .
