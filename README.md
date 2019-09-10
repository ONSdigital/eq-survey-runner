# eQ Census Survey Runner v3

[![Build Status](https://travis-ci.com/ONSdigital/eq-survey-runner.svg?branch=v3)](https://travis-ci.com/ONSdigital/eq-survey-runner)
[![codecov](https://codecov.io/gh/ONSdigital/eq-survey-runner/branch/v3/graph/badge.svg)](https://codecov.io/gh/ONSdigital/eq-survey-runner/branch/v3)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a2bc191a96e546b99a6d1c33b9b0ed62)](https://app.codacy.com/project/MebinAbraham/eq-survey-runner/dashboard?branchId=10869033)

This version of runner looks at optimising the service to accommodate the Census.
There are a number of major changes we need make to survey runner to develop the features required for the Census.
These changes are a combination of fixing technical debt we've built up and adding new features.
While these changes would be possible to implement in **_v2_**, having to develop them in such a way to be compatible with existing data and rolling deploys will add an un-acceptable overhead.

The changes we're aware of now:

-   architecture changes:

    -   block variants for proxy or past/present versions of content
    -   piping in structured schema rather than inlined jinja filters
    -   routing refactor for optimum performance
    -   redesign how repeating groups and association with driving questions works

-   new features:
    -   who lives here (collecting householders)
    -   relationships
    -   hub and spoke navigation
    -   look up patterns (address, occupation etc)

\*Existing **_v2_** schemas will be easily migrate-able to the new format when **_v3_** is stable.
This will be clearly documented and there is the possibility of scripts being provided to migrate schemas.
Once we know more about the implementation a decision will be made whether answer store migrations will be written for compatibility with existing data.\*

---

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

## Run locally

### Pre-Requisites

In order to run locally you'll need Node.js, snappy, pyenv and Jsonnet installed

```
brew install snappy npm pyenv jsonnet
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

To update the design system templates run:

```
make load-templates
```

Run the server inside the virtual env created by Pipenv with:

```
make run
```

### Supporting services

Runner requires three supporting services - a questionnaire launcher, a storage backend, and a cache.

#### Run supporting services with Docker

To run the app locally, but the supporting services in Docker, run:

```
make dev-compose-up
```

Note that on Linux you will need to use:

```
make dev-compose-up-linux
```

#### Run supporting services locally

##### Questionnaire launcher

https://github.com/ONSDigital/eq-questionnaire-launcher

```
docker run -e SURVEY_RUNNER_SCHEMA_URL=http://docker.for.mac.host.internal:5000 -it -p 8000:8000 eu.gcr.io/census-eq-ci/eq-questionnaire-launcher:latest
```

##### Storage backend

DynamoDB - https://github.com/ONSDigital/eq-docker-dynamodb

```
docker run -it -p 6060:8000 onsdigital/eq-docker-dynamodb:latest
```

or

Google Datastore - https://hub.docker.com/r/knarz/datastore-emulator/

```
docker run -it -p 8432:8432 knarz/datastore-emulator:latest
```

##### Cache

```
docker run -it -p 6379:6379 redis:4
```

#### Using Google Cloud Platform for supporting services

To use `EQ_STORAGE_BACKEND` as `datastore` or `EQ_SUBMISSION_BACKEND` as `gcs` directly on GCP and not a docker image, you need to set the GCP project using the following command:

```
gcloud config set project <gcp_project_id>
```

Or set the `GOOGLE_CLOUD_PROJECT` environment variable to your gcp project id.

---

## Frontend Tests

The frontend tests use NodeJS to run. You will need to have node version 8.X to run these tests. To do this, do the following commands:

```
brew install nvm
nvm install 8
nvm use 8
```

Install yarn with:

```
npm i -g yarn
```

Fetch npm dependencies (Note that this overrides the python version defined in `.python-version`):

```
PYENV_VERSION=system yarn
```

Available commands:

| Command                | Task                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| `yarn test_functional` | Runs the functional tests through ChimpJS (requires app running on localhost:5000 and generated pages). |
| `yarn test_cypress`    | Runs the Cypress functional tests (requires app running on localhost:5000 and generated pages).         |
| `yarn generate_pages`  | Generates the functional test pages.                                                                    |
| `yarn lint`            | Lints the JS, reporting errors/warnings.                                                                |
| `yarn format`          | Format the json schemas.                                                                                |

---

### Development with functional tests

The functional tests use Chimp (now [Chimpy](https://github.com/TheBrainFamily/chimpy)).

Underneath Chimp, the tests are written using [WebdriverIO](https://webdriver.io/docs), [Chai](https://www.chaijs.com/), and [Mocha](https://mochajs.org/)

### Functional test options

The functional tests use a set of selectors that are generated from each of the test schemas. These make it quick to add new functional tests.

To run the functional tests run :

`make test-functional`

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

```
./node_modules/cypress/bin/cypress open
```

---

## Deployment with [Helm](https://helm.sh/)

To deploy this application with helm, you must have a kubernetes cluster already running and be logged into the cluster.

Log in to the cluster using:

```
gcloud container clusters get-credentials survey-runner --region <region> --project <gcp_project_id>
```

You need to have Helm installed locally

1. Install Helm with `brew install kubernetes-helm` and then run `helm init --client-only`

2. Install Helm Tiller plugin for _Tillerless_ deploys `helm plugin install https://github.com/rimusz/helm-tiller`


### Deploying credentials

Before deploying the app to a cluster you need to create the application credentials on Kubernetes. Run the following command to provision the credentials:

```
EQ_KEYS_FILE=PATH_TO_KEYS_FILE EQ_SECRETS_FILE=PATH_TO_SECRETS_FILE ./k8s/deploy_credentials.sh
```

For example:

```
EQ_KEYS_FILE=dev-keys.yml EQ_SECRETS_FILE=dev-secrets.yml ./k8s/deploy_credentials.sh
```

### Deploying the app

The following environment variables can be set when deploying the app.
- SUBMISSION_BUCKET_NAME
- DOCKER_REGISTRY *(optional)*
- IMAGE_TAG *(optional)*
- GOOGLE_TAG_MANAGER_ID *(optional)*
- GOOGLE_TAG_MANAGER_AUTH *(optional)*
- GOOGLE_TAG_MANAGER_PREVIEW *(optional)*

To deploy the app to the cluster, run the following command:

```
./k8s/deploy_app.sh
```

For example:

```
SUBMISSION_BUCKET_NAME=census-eq-dev-1234567-survey-runner-submission ./k8s/deploy_app.sh
```

---

## Internationalisation

We use flask-babel to do internationalisation. To extract messages from source and create the messages.pot file, in the project root run the following command.

```
make translation-templates
```

This will extract messages and place them in the .pot files ready for translation.

These .pot files will then need to be translated. The translation process is documented in Confluence [here](https://collaborate2.ons.gov.uk/confluence/display/SDC/Translation+Process)

Once we have the translated .po files they can be added to the source code and used by the application

---

### Translating the schemas

The schemas can be translated assuming `.po` files are available. This can be done through the `scripts/translate_schemas.py` script.

## Environment Variables

The following env variables can be used

```
| Variable Name                             | Default               | Description                                                                                   |
|-------------------------------------------|-----------------------|-----------------------------------------------------------------------------------------------|
| EQ_LOG_LEVEL                              | INFO                  | The default logging level (defaults to 'INFO' for local development)                          |
| EQ_WERKZEUG_LOG_LEVEL                     | INFO                  | The default logging level for werkzeug (defaults to 'INFO' for local development)             |
| EQ_SESSION_TIMEOUT_SECONDS                | 2700 (45 mins)        | The duration of the flask session                                                             |
| EQ_PROFILING                              | False                 | Enables or disables profiling (True/False) Default False/Disabled                             |
| EQ_GOOGLE_TAG_MANAGER_ID                  |                       | The Google Tag Manger ID - Specifies the GTM account                                          |
| EQ_GOOGLE_TAG_MANAGER_AUTH                |                       | The Google Tag Manger Auth - Ties the GTM container with the whole enviroment                 |
| EQ_GOOGLE_TAG_MANAGER_PREVIEW             |                       | The Google Tag Manger Preview - Specifies the environment                                     |
| EQ_DEV_MODE                               | False                 | Enable dev mode                                                                               |
| EQ_ENABLE_FLASK_DEBUG_TOOLBAR             | False                 | Enable the flask debug toolbar                                                                |
| EQ_ENABLE_CACHE                           | True                  | Enable caching of the schema                                                                  |
| EQ_ENABLE_HTML_MINIFY                     | True                  | Enable minification of html                                                                   |
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
| EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS | 10000                 |                                                                                               |
| EQ_STORAGE_BACKEND                        | datastore             |                                                                                               |
| EQ_DATASTORE_EMULATOR_CREDENTIALS         | False                 |                                                                                               |
| EQ_DYNAMODB_ENDPOINT                      |                       |                                                                                               |
| EQ_REDIS_HOST                             |                       | Hostname of Redis instance used for ephemeral storage                                         |
| EQ_REDIS_PORT                             |                       | Port number of Redis instance used for ephemeral storage                                      |
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

---

## JWT Integration

Integration with the survey runner requires the use of a signed JWT using public and private key pair (see https://jwt.io,
https://tools.ietf.org/html/rfc7519, https://tools.ietf.org/html/rfc7515).

Once signed the JWT must be encrypted using JWE (see https://tools.ietf.org/html/rfc7516).

The JWT payload must contain the following claims:

-   exp - expiration time
-   iat - issued at time

The header of the JWT must include the following:

-   alg - the signing algorithm (must be RS256)
-   type - the token type (must be JWT)
-   kid - key identification (must be EDCRRM)

The JOSE header of the final JWE must include:

-   alg - the key encryption algorithm (must be RSA-OAEP)
-   enc - the key encryption encoding (must be A256GCM)

To access the application you must provide a valid JWT. To do this browse to the /session url and append a token parameter.
This parameter must be set to a valid JWE encrypted JWT token. Only encrypted tokens are allowed.

There is a python script for generating tokens for use in development, to run:

```
python token_generator.py
```

---

## Profiling

To profile the application run `make profile`. Profiling information will be collected per-request in the `profiling` directory where it can be examined using the Pstats Interactive Browser.

`$ python -m pstats <filename>`

will load the file into the interactive browser where it can be sorted and queried as required.

To visualise the profile, `snakeviz` can be used. This provides a nice interface with an icicle graph:

```
# First combine all the profiles in the 'profiling' directory.
# Ensure you delete all the files in this directory before starting your profiling session
# This will create a file called `combined_profile.prof`
pipenv run python scripts/merge_profiles.py

snakeviz combined_profile.prof
```

## Updating / Installing dependencies

To add a new dependency, use `pipenv install [package-name]`, which not only installs the package but Pipenv will also go to the trouble of updating the Pipfile as well.

NB: both the Pipfile and Pipfile.lock files are required in source control to accurately pin dependencies.
