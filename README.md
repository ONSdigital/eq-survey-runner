# Survey Runner - Foundation

* Based on python 3


[![Coverage Status](https://coveralls.io/repos/github/ONSdigital/eq-survey-runner/badge.svg?branch=master)](https://coveralls.io/github/ONSdigital/eq-survey-runner?branch=master)


## Setup

If using virtualenvwrapper (if not, you should be), create a new virtual env for python3

```
mkvirtual --python=`which python3` <your env name>
```

Install dependencies using pip

```
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

This will generate a JWT for you to log into the application. The script prints out the URL with the token included.

---

### Front-end Toolkit

The front-end toolkit uses nodejs, npm and gulp.

Install nodejs `5.4.x`. Make sure npm is installed with `npm`.

Install dependencies with:

```
npm install
```

Compile the project with
```
npm run compile
```

There are a few additional npm tasks:

Command                         | Task
--------------------------------|----------------------
`npm run compile`               | Build the assets (js, css, img) into `/app/static`
`npm run dev`                   | Build assets and watch for changes. Runs Browsersync.
`npm run test`                  | Runs the unit tests through Karma and the functional tests through a local Selenium instance
`npm run test_unit`             | Watches the unit tests via Karma
`npm run test_functional`       | Runs the functional tests through a local Selenium instance (requires app running on localhost:5000)
`npm run test_functional_sauce` | Runs the functional tests through Sauce Labs (requires app running on localhost:5000)
`npm run lint`                  | Lints the JS, reporting errors/warnings.

---

## Deployment with elastic beanstalk

You will need to install the EB CLI tools using PIP.

*NOTE:* The EB tools do not currently work with Python 3.5.  I installed the EB CLI tools *outside* my virtual environment and installed installed them globally using the following commands

```
deactivate                       # to exit the virtual environment
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
EQ_RABBITMQ_TEST_QUEUE_NAME - the name of the test queue
EQ_CLOUDWATCH_LOGGING - feature flag to enable AWS cloudwatch logging
EQ_GIT_REF - the latest git ref of HEAD on master
EQ_SR_LOG_GROUP - The name of the log group to create (defaults to `username-local` for local development)
EQ_LOG_LEVEL - The default logging level (defaults to 'INFO' for local development)
EQ_SCHEMA_DIRECTORY - The directory that contains the schema files
EQ_SESSION_TIMEOUT - The duration of the flask session, defaults to 30 minutes
EQ_SECRET_KEY - The Flask secret key for signing cookies
EQ_PROFILING - Enables or disables profiling (True/False) Default False/Disabled
EQ_UA_ID - The Google Analytics ID
EQ_SCHEMA_BUCKET - The name of the bucket in S3 where to look to find schemas.
```
## Loading schemas from S3

To enable an instance of the survey runner to load form schemas from AWS s3,
set the environment variable `EQ_SCHEMA_BUCKET` and ensure the correct IAM
permissions are set for the ec2 instances that are created by elasticbeanstalk
OR ensure you have the correct boto aws credentials set in `~/.aws/credentials`.

This will then make the schemas available in the dev page and enable the runner
to look inside the bucket to load schemas for rendering.

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
