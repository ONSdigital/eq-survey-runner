# eQ Census Survey Runner v3
[![Build Status](https://travis-ci.org/ONSdigital/eq-survey-runner.svg?branch=v3)](https://travis-ci.org/ONSdigital/eq-survey-runner)
[![codecov](https://codecov.io/gh/ONSdigital/eq-survey-runner/branch/v3/graph/badge.svg)](https://codecov.io/gh/ONSdigital/eq-survey-runner/branch/v3)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a2bc191a96e546b99a6d1c33b9b0ed62)](https://app.codacy.com/project/MebinAbraham/eq-survey-runner/dashboard?branchId=10869033)

This version of runner looks at optimising the service to accommodate the Census.
There are a number of major changes we need make to survey runner to develop the features required for the Census.
These changes are a combination of fixing technical debt we've built up and adding new features.
While these changes would be possible to implement in ***v2***, having to develop them in such a way to be compatible with existing data and rolling deploys will add an un-acceptable overhead.

The changes we're aware of now:

- architecture changes:
    - block variants for proxy or past/present versions of content
    - piping in structured schema rather than inlined jinja filters
    - routing refactor for optimum performance
    - redesign how repeating groups and association with driving questions works

- new features:
    - who lives here (collecting householders)
    - relationships
    - hub and spoke navigation
    - look up patterns (address, occupation etc)

*Existing ***v2*** schemas will be easily migrate-able to the new format when ***v3*** is stable.
This will be clearly documented and there is the possibility of scripts being provided to migrate schemas.
Once we know more about the implementation a decision will be made whether answer store migrations will be written for compatibility with existing data.*

---
## Getting Set Up

### Run with Docker
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

To run the unit tests locally:
```
pipenv run scripts/run_tests_unit.sh
```


### Pre-Requisites
In order to run locally you'll need PostgreSQL, Node.js, sqlite3, snappy and pyenv installed

```
brew install postgres snappy npm sqlite3 pyenv
```

Note that npm currently requires Python 2.x for some of the setup steps,
it doesn't work with Python 3.

### Setup
It is preferable to use the version of Python locally that matches that
used on deployment. This project has a `.python_version` file for this
purpose.


Upgrade pip and install dependencies:

```
pyenv install
pip install --upgrade pip setuptools pipenv
pipenv install --dev
```

Run the server inside the virtual env created by Pipenv with:

```
pipenv run ./scripts/run_app.sh
```

Note, you will also need to run an upstream tool (eg, https://github.com/ONSDigital/go-launch-a-survey) to launch a survey.

```
docker run -e SURVEY_RUNNER_SCHEMA_URL=http://docker.for.mac.host.internal:5000 -it -p 8000:8000 onsdigital/go-launch-a-survey:latest
```

This will generate a JWT for you to log into the application.

The data storage backend is configurable with the `EQ_STORAGE_BACKEND` environment variable. You will need to run an emulator if you are setting this to DynamoDB or Google Datastore:

DynamoDB: <https://github.com/ONSDigital/eq-docker-dynamodb>

Google Datastore: <https://hub.docker.com/r/knarz/datastore-emulator/>

```
docker run -it -p 6060:8000 onsdigital/eq-docker-dynamodb:latest
OR
docker run -it -p 8432:8432 knarz/datastore-emulator:latest
```

Please note that currently the SQL backend does not support submitted responses

---

To use `EQ_STORAGE_BACKEND` as `datastore` or `EQ_SUBMISSION_BACKEND` as `gcs` directly on GCP and not a docker image, you need to set the GCP project using the following command:
```
gcloud config set project <gcp_project_id>
```
Or set the `GOOGLE_CLOUD_PROJECT` environment variable to your gcp project id.

---

#### Front-end Toolkit

The front-end toolkit uses nodejs, yarn and gulp.

Currently, in order to build the front-end toolkit, you will need to have node version 8.X.  To do this, do the following commands:
```
brew install nvm
nvm install 8
nvm use 8
```

Install yarn with:

```
npm install yarn --global
```

Fetch npm dependencies (Note that this overrides the python version defined in `.python-version`):

```
PYENV_VERSION=system yarn
```

Compile the project with
```
yarn compile
```

There are a few additional npm tasks:

Command                                    | Task
-------------------------------------------|----------------------
`yarn compile`                          | Build the assets (js, css, img) into `/static`.
`yarn dev`                              | Build assets and watch for changes. Runs Browsersync.
`yarn test`                             | Runs the unit tests through Karma and the functional tests through a local Selenium instance.
`yarn test_unit`                        | Watches the unit tests via Karma.
`yarn test_functional`                  | Runs the functional tests through ChimpJS (requires app running on localhost:5000 and generated pages).
`yarn test_cypress`                     | Runs the Cypress functional tests (requires app running on localhost:5000 and generated pages).
`yarn generate_pages`                   | Generates the functional test pages.
`yarn lint`                             | Lints the JS, reporting errors/warnings.
`yarn format`                           | Format the json schemas.

---

###
Upgrade usage of the pattern library
(Currently) To make an upgrade to the pattern library you'll need to change the short-hand commit hash in the following files:
* app/assets/favicons/browserconfig.xml `<square150x150logo src="https://cdn.ons.gov.uk/sdc/[COMMIT HASH HERE]/favicons/mstile-150x150.png"/>`
* app/assets/styles/partials/vars/_vars.scss.xml `$cdn-url-root: "https://cdn.ons.gov.uk/sdc/[COMMIT HASH HERE]";`
* app/templates/layouts/base.html `{% set cdn_hash = "[COMMIT HASH HERE]" %}`

### Functional test options

The functional tests use a set of selectors that are generated from each of the test schemas. These make it quick to add new functional tests.

To run the functional tests use the script:

`./scripts/run_tests_functional.sh`

This will delete the `tests/functional/generated_pages` directory and regenerate all the files in it from the schemas.

You can also individually run the `generate_pages` and `test_functional` yarn scripts:

`yarn generate_pages; yarn test_functional`

To generate the pages manually you can run the `generate_pages` scripts with the schema directory. Run it from the `tests/functional` directory as follows:

`./generate_pages.py ../../data/en/ ./generated_pages -r "../../base_pages"`

To generate a spec file with the imports included, you can use the `generate_pages.py` script on a single schema with the `-s` argument.

`./generate_pages.py ../../data/en/test_multiple_piping.json ./temp_directory -r "../../base_pages" -s spec/test_multiple_piping.spec.js`

If you have already built the generated pages, then the functional tests can be executed with:

`yarn test_functional`

This can be limited to tests under a directory with:

`yarn test_functional --path tests/functional/spec/components/`

To run a single test, add `@watch` into the name of any `describe` or `it` function and run:

`yarn test_functional --watch`

An example of adding `@watch` looks like this:
`describe('@watch Skip Conditions', function() {...}` or
`it('@watch Given this is a test', function() {...}`

To run the tests against a remote deployment you will need to specify the environment variable of EQ_FUNCTIONAL_TEST_ENV eg:

`EQ_FUNCTIONAL_TEST_ENV=https://staging-new-surveys.dev.eq.ons.digital/ yarn test_functional`

To run the census functional tests within the cypress UI:

./node_modules/cypress/bin/cypress open

### Deployment with [Helm](https://helm.sh/)

To deploy this application with helm, you must have a kubernetes cluster already running and be logged into the cluster.

Log in to the cluster using:
```
gcloud container clusters get-credentials survey-runner --region <region> --project <gcp_project_id>
```
You need to have Helm installed locally

1. Install Helm with `brew install kubernetes-helm` and then run `helm init --client-only`

1. Install Helm Tiller plugin for *Tillerless* deploys `helm plugin install https://github.com/rimusz/helm-tiller`

Before deploying the app to a cluster you need to create the application credentials on Kubernetes. Run the following command to provision the credentials:

```
EQ_KEYS_FILE=PATH_TO_KEYS_FILE EQ_SECRETS_FILE=PATH_TO_SECRETS_FILE ./k8s/deploy_credentials.sh
```
##### Example
```
EQ_KEYS_FILE=docker-keys.yml EQ_SECRETS_FILE=docker-secrets.yml ./k8s/deploy_credentials.sh
```
---

To deploy the app to the cluster, run the following command:
```
./k8s/deploy_app.sh <SUBMISSION_BUCKET_NAME> <DOCKER_REGISTRY> <IMAGE_TAG>
```
##### Example
 ```
./k8s/deploy_app.sh census-eq-dev-1234567-survey-runner-submission eu.gcr.io/census-eq-dev v3.0.0
 ```
 
### Internationalisation

We use flask-babel to do internationalisation.  To extract messages from source, in the project root run the following command.

```
pipenv run pybabel extract -F babel.cfg -o app/translations/messages.pot .
```

This will extract messages and place them in the translations/messages.pot file ready for translation.

You should only need to create the language files once.

To create Welsh language files, run the following command

```
pipenv run pybabel init -i app/translations/messages.pot -d app/translations -l cy
```

To create the gaelic language files, use the following:

```
pipenv run pybabel init -i app/translations/messages.pot -d app/translations -l gd
```

#### Getting text translated

Our current language translation service requires a .csv rather than a .po file. To convert a .po file to a .csv you'll need to install the Python translate-toolkit:
```
brew install translate-toolkit
```

To generate the .csv file:
```
po2csv app/translations/cy/LC_MESSAGES/messages.po app.translations/static-cy.csv
```

To convert back to a .po file:
```
csv2po app.translations/static-cy.csv app/translations/cy/LC_MESSAGES/messages.po
```

*Important:* There are some encoding issues when opening the .csv file in Excel. Opening in Google sheets and saving as a .xslx file resolves this.

#### Compiling the translations

To compile the language files for use in the application, use the following:

```
pipenv run pybabel compile -d app/translations
```

As strings are added to the application, you will need to update but not overwrite the translations for the various languages.
To update the language strings, use:

```
pipenv run pybabel update -i app/translations/messages.pot -d app/translations
```

### Environment Variables

The following env variables can be used
```
| Variable Name                             | Default               | Description                                                                                   |
|-------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------|
| EQ_LOG_LEVEL                              | INFO                  | The default logging level (defaults to 'INFO' for local development)                          |
| EQ_WERKZEUG_LOG_LEVEL                     | INFO                  | The default logging level for werkzeug (defaults to 'INFO' for local development)             |
| EQ_SESSION_TIMEOUT_SECONDS                | 2700 (45 mins)        | The duration of the flask session                                                             |
| EQ_PROFILING                              | False                 | Enables or disables profiling (True/False) Default False/Disabled                             |
| EQ_UA_ID                                  |                       | The Google Analytics ID                                                                       |
| EQ_DEV_MODE                               | False                 | Enable dev mode                                                                               |
| EQ_ENABLE_FLASK_DEBUG_TOOLBAR             | False                 | Enable the flask debug toolbar                                                                |
| EQ_ENABLE_CACHE                           | True                  | Enable caching of the schema                                                                  |
| EQ_ENABLE_SECURE_SESSION_COOKIE           | True                  | Set secure session cookies                                                                    |
| EQ_MAX_HTTP_POST_CONTENT_LENGTH           | 65536                 | The maximum http post content length that the system wil accept                               |
| EQ_DEVELOPER_LOGGING                      | False                 | Enable developer style logging described here                                                 |
                                                                    | http://structlog.readthedocs.io/en/stable/development.html                                    |
| EQ_MINIMIZE_ASSETS                        | True                  | Should JS and CSS be minimized                                                                |
| MAX_CONTENT_LENGTH                        | 65536                 | max request payload size in bytes                                                             |
| EQ_APPLICATION_VERSION_PATH               | .application-version  | the location of a file containing the application version number                              |
| EQ_ENABLE_LIVE_RELOAD                     | False                 | Enable livereload of browser when scripts, styles or templates are updated                    |
| EQ_SECRETS_FILE                           | secrets.yml           | The location of the secrets file                                                              |
| EQ_KEYS_FILE                              | keys.yml              | The location of the keys file                                                                 |
| EQ_SUBMISSION_BACKEND                     |                       | Which submission backed to use ( gcs, rabbitmq, log )                                         |
| EQ_GCS_SUBMISSION_BUCKET_ID               |                       | The Bucket id in Google cloud platform to store the submissions in                            |
| EQ_RABBITMQ_HOST                          |                       |                                                                                               |
| EQ_RABBITMQ_HOST_SECONDARY                |                       |                                                                                               |
| EQ_RABBITMQ_PORT                          | 5672                  |                                                                                               |
| EQ_RABBITMQ_QUEUE_NAME                    | submit_q              | The name of the submission queue                                                              |
| EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER    | postgresql            |                                                                                               |
| EQ_SERVER_SIDE_STORAGE_DATABASE_HOST      |                       |                                                                                               |
| EQ_SERVER_SIDE_STORAGE_DATABASE_PORT      | 5432                  |                                                                                               |
| EQ_SERVER_SIDE_STORAGE_DATABASE_NAME      | digitaleqrds          |                                                                                               |
| EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS | 10000                 |                                                                                               |
| SQLALCHEMY_DATABASE_URI                   |                       | a Database URI to use to connecto to a database                                               |
| EQ_STORAGE_BACKEND                        | datastore             |                                                                                               |
| EQ_DATASTORE_EMULATOR_CREDENTIALS         | False                 |                                                                                               |
| EQ_DYNAMODB_ENDPOINT                      |                       |                                                                                               |
| EQ_DYNAMODB_MAX_RETRIES                   | 5                     |                                                                                               |
| EQ_DYNAMODB_MAX_POOL_CONNECTIONS          | 30                    |                                                                                               |
| EQ_SUBMITTED_RESPONSES_TABLE_NAME         |                       |                                                                                               |
| EQ_QUESTIONNAIRE_STATE_TABLE_NAME         |                       |                                                                                               |
| EQ_SESSION_TABLE_NAME                     |                       |                                                                                               |
| EQ_USED_JTI_CLAIM_TABLE_NAME              |                       |                                                                                               |
| EQ_NEW_RELIC_ENABLED                      | False                 | Enable New Relic monitoring                                                                   |
| NEW_RELIC_LICENSE_KEY                     |                       | Enable new relic monitoring by supplying a New Relic licence key                              |
| NEW_RELIC_APP_NAME                        |                       | The name to display for the application in New Relic                                          |
```

The following env variables can be used when running tests
```
EQ_FUNCTIONAL_TEST_ENV - the pre-configured environment [local, docker, preprod] or the url of the environment that should be targeted
```

### JWT Integration
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

### Profiling

Setting the `EQ_PROFILING` environment variable to `True` will enable profiling of the application.  Profiling information
will be collected per-request in the `profiling` directory where it can be examined using the Pstats Interactive Browser.

`$ python -m pstats <filename>`

will load the file into the interactive browser where it can be sorted and queried as required.

To visualise the profile, `snakeviz` can be used. This provides a nice interface with an 'icicle' graph:

```
# First combine all the profiles in the 'profiling' directory.
# Ensure you delete all the files in this directory before starting your profiling session
# This will create a file called `combined_profile.prof`
pipenv run python scripts/merge_profiles.py

snakeviz combined_profile.prof
```

### Updating / Installing dependencies

To add a new dependency, use `pipenv install [package-name]`, which not only installs the package but Pipenv will also go to the trouble of updating the Pipfile as well.

NB: both the Pipfile and Pipfile.lock files are required in source control to accurately pin dependencies.

### Alpha Survey Runner
If you're looking for the Survey Runner code from the Alpha then it has been renamed to: alpha-eq-survey-runner
- https://github.com/ONSdigital/alpha-eq-survey-runner
