<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![Codacy][codacy-shield]][codacy-url]
[![Codecov][coverage-shield]][coverage-url]
[![Functional Tests][functional-tests-shield]][functional-tests-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">


  <h3 align="center">Electronic Questionnaire <br />(EQ) (Runner)</h3>

  <p align="center">An application enabling respondents to digitally complete questionnaires.</p>
</div>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#roadmap">Roadmap</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#api-reference">API Reference</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#compiling-the-front-end">Compiling the Frontend</a></li>
    <li><a href="#additional-yarn-commands">Additional Yarn Commands</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Electronic questionnaire, also known as EQ, Runner, or EQ/Runner, is a frontend application that enables respondents to digitally complete a questionnaire. 


### Built With

* [Python](https://www.python.org/downloads/)
* [Node](https://nodejs.org/en/)
* [Npm](https://www.npmjs.com/get-npm)
* [Postgres](https://www.postgresql.org/)
* [Snappy](https://github.com/google/snappy)
* [Pyenv](https://github.com/pyenv/pyenv)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
* [Docker](https://www.docker.com/)
* [Docker-Compose](https://docs.docker.com/compose/install/)

### Roadmap

As [Electronic Questionnaire (EQ) (Runner) version 3](https://github.com/ONSdigital/eq-questionnaire-runner) is being developed, we are no longer actively progressing this product. However, if you spot any critical bugs or would grately benefit from an additional feature, please get in touch.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Booting up the application through Docker Compose is the easiest method. Therefore, ensure that you have [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/install/) installed. Then, progress to the installation steps.

Alternatively, in order to run locally you'll need PostgreSQL, Node.js, sqlite3, snappy and pyenv installed.
* Via [Homebrew](https://brew.sh/):
  ```sh
  ➜ brew install postgres snappy npm sqlite3 pyenv
  ```

### Installation

Docker is the easiest way of booting up the application. However, if you want, you can also run it outside of Docker as well.

#### Method one - using Docker

If you use this method, you will also be spinning up all of the necessary tools to let EQ function locally, including an instance of [go-launch-a-survey](https://github.com/ONSdigital/go-launch-a-survey), which is necessary for accessing the questionnaires in EQ.

1. Clone the repo
   * SSH (preferred)
   ```sh
   ➜ git clone git@github.com:ONSdigital/eq-survey-runner.git
   ```
      * HTTP:
   ```sh
   ➜ git clone https://github.com/ONSdigital/eq-survey-runner.git
   ```
2. Install NPM packages
   ```sh
   ➜ npm install
   ```
3. Run the following command, passing the `--build` flag the first time.
   ```sh
	➜ docker-compose up
   ```
	
#### Method 2 - locally

Using this method requires you to use multiple different terminal windows. We have found that [iTerm2](https://iterm2.com/) is a good solution for managing them; allowing you to organise them into panes within a single window.

1. Open a terminal window; these next steps will take you through booting up EQ.
2. Upgrade pip and install dependencies.
	 ```sh
	   ➜ pyenv install
       ➜ pip install --upgrade pip setuptools pipenv
       ➜ pipenv install --dev
   ```
3. Run the server inside the virtual env created by Pipenv.
   ```sh
   ➜ pipenv run ./scripts/run_app.sh
   ```
4. Open a new terminal window; this next step will take you through spinning up [go-launch-a-survey](https://github.com/ONSdigital/go-launch-a-survey), which is necessary for accessing the questionnaires in EQ.
5. Spin up an instance of [go-launch-a-survey](https://github.com/ONSdigital/go-launch-a-survey) from [it's Dockerhub image](https://hub.docker.com/r/onsdigital/go-launch-a-survey/).
   ```sh
   ➜ docker run -e SURVEY_RUNNER_SCHEMA_URL=http://docker.for.mac.host.internal:5000 -it -p 8000:8000 onsdigital/go-launch-a-survey:latest
   ```
6. Open a new terminal window. This next step will take you through spinning up a DynamoDB instance, which is necessary to simulate submitting questionnaires.
7. Spin up a DynamoDB instance from [it's Dockerhub image](https://hub.docker.com/r/onsdigital/eq-docker-dynamodb).
   ```sh
   ➜ docker run -it -p 6060:8000 onsdigital/eq-docker-dynamodb:latest
   ```

<!-- USAGE EXAMPLES -->
## Usage

Once installed and running, you can navigate to `http://localhost:8000/`. This will take you to [go-launch-a-survey](https://github.com/ONSdigital/go-launch-a-survey), which allows you to view questionnaires as a respondent would in production.

If you have a DynamoDB view installed (we reccomend [DynamoDB Admin](https://www.npmjs.com/package/dynamodb-admin)), you can point it at `http://localhost:6060` to view the contents of EQs databases.

<!-- API Reference -->
## API Reference

Electronic Questionnaire comes with a minor API which allows interaction with it's databases. Requests to the API should be pointed at `http://localhost:5000`.

### POST /flush
Flushes a single partial response.

**You send**: a JSON object of the following format, encoded within a JWT token, sent as a query parameter. **You get**: confirmation as to whether or not the flushing succeeded.

#### Request:

Headers
```
POST /flush HTTP/1.1
Accept: */*
Content-Length: 0
```
Params
```
token: (some JWT token)
```

#### Successful Response:
```
HTTP/1.1 200 OK
```

#### Failed Response
The endpoint responds with a `404` if the user described in the JWT has no partial response to flush.
```
HTTP/1.1 404 Not found
```

The endpoint responds with a `403` if the request did not include the appropriate role 'flusher'.
```
HTTP/1.1 403 Forbidden
```

### POST /flush_collection

Flushes all partial responses for a specified collection exercise.

**You send**: a JSON object of the following format, encoded within a JWT token, sent as a query parameter. **You get**: confirmation as to whether or not the flushing succeeded and to which partial responses were or were not flushed.

JSON object format to be encoded within a JWT:
```
{
	'collection_exercise_id': STRING
}
```

#### Request:

Headers
```
POST /flush_collection HTTP/1.1
Accept: */*
Content-Length: 0
```
Params
```
token: (some JWT token)
```

#### Successful Response:
```
HTTP/1.1 200 OK

{
	'collection_exercise_id': STRING,
	'total_partial_responses': INT,
	'successful_flush: [
		{
			'user_id': STRING,
			'ru_ref': STRING,
			'eq_id': STRING,
			'form_type': STRING,
		}
	],
	'failed_flush: [
		{
			'user_id': STRING,
			'ru_ref': STRING,
			'eq_id': STRING,
			'form_type': STRING,
		}
	]
}
```

#### Failed Response
The endpoint responds with a `400` if the `token` param could not be found, or if the `collection_exercise_id` param could not be found within the decrypted JWT token.
```
HTTP/1.1 400 Bad Request

Could not find expected request argument: token
```
```
HTTP/1.1 400 Bad Request

Could not find "collection_exercise_id" in decrypted JWT
```

The endpoint responds with a `403` if the JWT token given could not be decrypted.
```
HTTP/1.1 403 Forbidden

Failed to decrypt given token
```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

> If your contribution stems from a Jira ticket, please make sure to format your feature branch name as `JiraTicketId-AmazingFeature`.

1. Create your Feature Branch (`git checkout -b feature-AmazingFeature`)
2. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the Branch (`git push origin feature-AmazingFeature`)
4. Open a Pull Request

## Compiling the Frontend

The front-end does not recompile automatically when the source code changes. Whenever you make any visual changes, or the first time you spin up the application (it should be done already, but it's always better to be safe than sorry), do the following:

1. Install [Node Version Manager](https://github.com/nvm-sh/nvm) and temporarily swap your node version to 8. (The toolkit requires version 8 of node to run propperly).
   ```sh
   ➜ brew install nvm
   ➜ nvm install 8
   ➜ nvm use 8
   ```
2. Install [Yarn](https://yarnpkg.com/)
   ```sh
   ➜ npm install yarn --global
   ```
3. Fetch NPM dependencies (Note that this overrides the python version defined in `.python-version`).
   ```sh
   ➜ PYENV_VERSION=system yarn
   ```
4. Compile
   ```sh
   ➜ yarn compile
   ```
5. Swap back to your original version of Node.
   ```sh
   ➜ nvm use <node version>
   ```

## Additional Yarn Commands

|Command | Task|
|-------------------------------------------|----------------------|
|`yarn compile` | Build the assets (js, css, img) into `/static`.|
|`yarn dev` | Build assets and watch for changes. Runs Browsersync.|
|`yarn test` | Runs the unit tests through Karma and the functional tests through a local Selenium instance.|
|`yarn test_unit` | Watches the unit tests via Karma.|
|`yarn test_functional` | Runs the functional tests through ChimpJS (requires app running on localhost:5000 and generated pages).|
|`yarn generate_pages` | Generates the functional test pages.|
|`yarn lint` | Lints the JS, reporting errors/warnings.|
|`yarn format` | Format the json schemas.|

   
<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/ONSdigital/eq-survey-runner.svg?style=for-the-badge
[license-url]: https://github.com/ONSdigital/eq-survey-runner/blob/master/LICENSE

[coverage-shield]: https://img.shields.io/codecov/c/github/ONSdigital/eq-survey-runner?style=for-the-badge
[coverage-url]: https://codecov.io/gh/ONSdigital/eq-survey-runner

[codacy-shield]: https://img.shields.io/codacy/coverage/82e63fc5bc5c43e8ba1ba6d13bfb4243?label=Codacy&style=for-the-badge
[codacy-url]: https://app.codacy.com/manual/ONSDigital/eq-survey-runner/dashboard?branch=master

[functional-tests-shield]: https://img.shields.io/github/workflow/status/ONSdigital/eq-survey-runner/EQ%20functional%20tests?label=Functional%20tests&style=for-the-badge
[functional-tests-url]: https://github.com/ONSdigital/eq-survey-runner/actions?query=workflow%3A%22EQ+functional+tests%22
