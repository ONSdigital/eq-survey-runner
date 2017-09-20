# eQ Survey Runner
[![Build Status](https://travis-ci.org/ONSdigital/eq-survey-runner.svg?branch=master)](https://travis-ci.org/ONSdigital/eq-survey-runner) [![codecov](https://codecov.io/gh/ONSdigital/eq-survey-runner/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/eq-survey-runner) [![Dependency Status](https://gemnasium.com/badges/github.com/ONSdigital/eq-survey-runner.svg)](https://gemnasium.com/github.com/ONSdigital/eq-survey-runner) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/82e63fc5bc5c43e8ba1ba6d13bfb4243)](https://www.codacy.com/app/ONSDigital/eq-survey-runner)

## Run with Docker
Install Docker for your system: https://www.docker.com/

To get eq-survey-runner running the following command will build and run the containers
```
docker-compose up -d
```

To launch a survey, navigate to `http://localhost:8000/`

When the containers are running you are able to access the application as normal, and code changes will be reflected in the running application.
However, any new dependencies that are added would require a re-build.

To rebuild the eq-survey-runner container, the following command can be used.
```
docker-compose build
```

If you need to rebuild the container from scratch to re-load any dependencies then you can run the following
```
docker-compose build --no-cache
```

To run just the unit tests inside Docker:
```
docker build -t onsdigital/eq-survey-runner .
docker build -t onsdigital/eq-survey-runner-unit-tests -f Dockerfile.test .
docker run onsdigital/eq-survey-runner-unit-tests
```


## Pre-Requisites
In order to run locally you'll need PostgreSQL and Node.js installed

PostgreSQL
```
brew install postgres
```

npm
```
brew install npm
```

Note that npm currently requires Python 2.x for some of the setup steps,
it doesn't work with Python 3.

## Setup
It is preferable to use the version of Python locally that matches that
used on deployment. This project has a `.python_version` file for this
purpose.

If you are using pyenv (https://github.com/yyuu/pyenv), you can install
the correct version of Python alongside any existing versions easily:

```
pyenv install
```

You should also use a virtualenv (https://github.com/yyuu/pyenv-virtualenv)
to keep this project's package installations separate from others you
are working on, to create a new virtualenv:

```
pyenv virtualenv <your env name>
pyenv activate <your env name>
```

Upgrade pip and install dependencies:

```
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

If you need to run the tests:
```
pip install -r requirements_for_test.txt
```

Run the server with

```
./scripts/run_app.sh

```

Note, you will also need to run an upstream tool (eg, https://github.com/ONSDigital/go-launch-a-survey) to launch a survey.
 
```
docker run -it -p 8000:8000 onsdigital/go-launch-a-survey:latest
```

This will generate a JWT for you to log into the application.

---

### Front-end Toolkit

The front-end toolkit uses nodejs, yarn and gulp.

Install yarn with:

```
npm install yarn --global
```

Compile the project with
```
yarn compile
```

There are a few additional npm tasks:

Command                                    | Task
-------------------------------------------|----------------------
`yarn compile`                          | Build the assets (js, css, img) into `/static`
`yarn dev`                              | Build assets and watch for changes. Runs Browsersync.
`yarn test`                             | Runs the unit tests through Karma and the functional tests through a local Selenium instance
`yarn test_unit`                        | Watches the unit tests via Karma
`yarn test_functional`                  | Runs the functional tests through a local Selenium instance (requires app running on localhost:5000)
`yarn test_functional_sauce`            | Runs the functional tests through Sauce Labs (requires app running on localhost:5000)
`yarn test_functional_browserstack`     | Runs the functional tests through BrowserStack (requires app running on localhost:5000)
`yarn lint`                             | Lints the JS, reporting errors/warnings.
`yarn format`                           | Format the json schemas.

---

## Functional test options

To create functional test pages from a schema use the following command.

`generate_pages.py <schema.json> <page_directory>` 

This can combined with `-spec_file=<spec_file_path>` to provide a populated template for the functional tests spec file.
and/or `-require_path='../..` To provide a relative path from a page file to the directory containing the base/parent page classes. Defaults to ".."

For example: 
`./generate_pages.py ../../data/en/test_navigation.json ./pages/surveys/navigation --spec_file=./spec/navigation.spec.js` 

The functional tests can be executed with a couple of options.

`--env=preprod` Will run the test against preprod.
`--spec=mci` Will run a single test spec (`mci.spec.js`) instead of the entire suite.
`--suite=core` Will run a suite of tests (core) instead of the entire suite.

These options can be combined with `test_functional` or `test_functional_sauce`, eg:

`yarn test_functional_sauce -- --env=preprod --spec=mci` Will run the MCI spec against preprod via SauceLabs.

*NOTE:* You will need the appropriate environment variables to be able to connect to SauceLabs.

## Deployment with elastic beanstalk

You will need to install the EB CLI tools using PIP.

*NOTE:* The EB tools do not currently work with Python 3.5.  I installed the EB CLI tools *outside* my virtual environment and installed installed them globally using the following commands

```
pyenv deactivate                 # to exit the virtual environment
sudo pip install awsebcli        # install the eb cli tools
```

Using the Elastic Beanstalk CLI is quite simple but mus tbe done *outside* the virtual environment of the project itself.  It will use the requirements.txt to ensure any requirements are at the right version for the deployed application.

Initialise the project using the command

```
eb init --region eu-west-1
```

This will launch a wizard asking for the AWS credentials and some questions about the environment to create.

`eu-west-1` is the name for Ireland.  I chose the default application name.

Once completed, you can then deploy the application using the following command:

```
eb create
```

This will create the environment and spin up the application . Once the application has deployed you can use the following command to open it in a browser

```
eb open
```

## Internationalisation

We use flask-babel to do internationalisation.  To extract messages from source, in the project root run the following command.

```
pybabel extract -F babel.cfg -o app/translations/messages.pot .
```

This will extract messages and place them in the translations/messages.pot file ready for translation.

You should only need to create the language files once.

To create Welsh language files, run the following command

```
pybabel init -i app/translations/messages.pot -d translations -l cy
```

To create the gaelic language files, use the following:

```
pybabel init -i app/translations/messages.pot -d translations -l gd
```

To compile the language files for use in the application, use the following:

```
pybabel compile -d translations
```

As strings are added to the application, you will need to update but not overwrite the translations for the various languages.
To update the language strings, use:

```
pybabel update -i app/translations/messages.pot -d translations
```

## Environment Variables

The following env variables can be used
```
EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY - the RRM public key for JWT user authentication
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY - the SR private key for JWT user authentication
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD - password of the SR private key for JWT user authentication
EQ_SUBMISSION_SDX_PUBLIC_KEY - the SDX public key for encryption of Submission data
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY - the SR private key for signing of submission data
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD - the password to the SR private key
EQ_RABBITMQ_URL - the RabbitMQ connection string
EQ_RABBITMQ_QUEUE_NAME - the name of the submission queue
EQ_SERVER_SIDE_STORAGE_DATABASE_URL - url of the database to connect to, e.g. 'sqlite:////tmp/questionnaire.db')
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_COUNT - Number of times to retry setting up the database (connection/creation) if it fails
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_DELAY_SECONDS - Number of seconds to wait between retry attempts to setup the database
EQ_LOG_LEVEL - The default logging level (defaults to 'INFO' for local development)
EQ_WERKZEUG_LOG_LEVEL - The default logging level for werkzeug (defaults to 'INFO' for local development)
EQ_SCHEMA_DIRECTORY - The directory that contains the schema files
EQ_SESSION_TIMEOUT_SECONDS - The duration of the flask session
EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS - The grace period between when the server removes the session and what we tell the client
EQ_SECRET_KEY - The Flask secret key for signing cookies
EQ_PROFILING - Enables or disables profiling (True/False) Default False/Disabled
EQ_UA_ID - The Google Analytics ID
EQ_SCHEMA_BUCKET - The name of the bucket in S3 where to look to find schemas
SAUCE_USERNAME - Sauce Labs username
SAUCE_ACCESS_KEY - Sauce Labs private key
EQ_DEV_MODE - Enable dev mode
EQ_ENABLE_FLASK_DEBUG_TOOLBAR - Enable the flask debug toolbar
EQ_ENABLE_CACHE - Enable caching of the schema
EQ_MAX_HTTP_POST_CONTENT_LENGTH - The maximum http post content length that the system wil accept
EQ_MAX_NUM_REPEATS - The maximum number of repeats the system will allow
EQ_DEVELOPER_LOGGING - Enable developer style logging described here http://structlog.readthedocs.io/en/stable/development.html

EQ_NEW_RELIC_ENABLED - Enable New Relic monitoring
NEW_RELIC_LICENSE_KEY - Enable new relic monitoring by supplying a New Relic licence key
NEW_RELIC_APP_NAME - The name to display for the application in New Relic
```

The following env variables can be used when running tests
```
EQ_FUNCTIONAL_TEST_ENV - the pre-configured environment [local, docker, preprod] or the url of the environment that should be targeted
```

## JWT Integration
Integration with the survey runner requires the use of a signed JWT using public and private key pair (see https://jwt.io,
https://tools.ietf.org/html/rfc7519, https://tools.ietf.org/html/rfc7515).

Once signed the JWT must be encrypted using JWE (see https://tools.ietf.org/html/rfc7516).

The JWT payload must contain the following claims:
- exp - expiration time
- iat - issued at time

The header of the JWT must include the following:
- alg - the signing algorithm (must be RS256)
- type - the token type (must be JWT)
- kid - key identification  (must be EDCRRM)

The JOSE header of the final JWE must include:
- alg - the key encryption algorithm (must be RSA-OAEP)
- enc - the key encryption encoding (must be A256GCM)

To access the application you must provide a valid JWT. To do this browse to the /session url and append a token parameter.
This parameter must be set to a valid JWE encrypted JWT token. Only encrypted tokens are allowed.

There is a python script for generating tokens for use in development, to run:
```
python token_generator.py
```

## profiling

Setting the `EQ_PROFILING` environment variable to `True` will enable profiling of the application.  Profiling information
will be collected per-request in the `profiling` directory where it can be examined using the Pstats Interactive Browser.

`$ python -m pstats <filename>`

will load the file into the interactive browser where it can be sorted and queried as required.

## Updating / Installing dependencies

We make use of python pip's support for only installing packages if their sha-256 hash matches a known good value.
To add a new dependency, try installing the `hashin` python package that calculates a hash and adds it to the
local `requirements.txt`. When installing the dependencies, always use `--require-hashes` to force this check
on downloaded packages.

## Alpha Survey Runner
If you're looking for the Survey Runner code from the Alpha then it has been renamed to: alpha-eq-survey-runner
- https://github.com/ONSdigital/alpha-eq-survey-runner
