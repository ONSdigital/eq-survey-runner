# Survey Runner - Foundation

* Based on python 3

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

Command            | Task
-------------------|----------------------
`npm run compile`  | Build the assets (js, css, img) into `/app/static`
`npm run dev`      | Build assets and watch for changes. Runs Browsersync.
`npm run test`     | Runs the test suite through Karma.
`npm run lint`     | Lints the JS, reporting errors/warnings.

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
EQ_RRM_PUBLIC_KEY - location on disk of the RRM public key
EQ_SR_PRIVATE_KEY - location on disk of the SR private key
EQ_RABBITMQ_URL - the RabbitMQ connection string
EQ_RABBITMQ_QUEUE_NAME - the name of the submission queue
EQ_RABBITMQ_TEST_QUEUE_NAME - the name of the test queue
EQ_PRODUCTION - flag to indicate if we're running in production or dev mode
EQ_GIT_REF - the latest git ref of HEAD on master
EQ_SR_LOG_GROUP - The name of the log group to create (defaults to `username-local` for local development)
EQ_LOG_LEVEL - The default logging level (defaults to 'INFO' for local development)
EQ_SCHEMA_DIRECTORY - The directory that contains the schema files
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

When running in production mode every request to the survey runner must append the follow url parameter: `token`. This
parameter must be set to a valid JWE encrypted JWT token. Only encrypted tokens are allowed in production mode.

When running in dev mode the token is not mandatory, however it can be supplied and if so will be decrypted/decoded and
used. Also when in dev mode, unencrypted signed and unencrypted unsigned tokens can be also used in the url parameter
'token'.


## Alpha Survey Runner
If you're looking for the Survey Runner code from the Alpha then it has been renamed to: alpha-eq-survey-runner
- https://github.com/ONSdigital/alpha-eq-survey-runner
