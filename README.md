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

Run the server with

```
python runner.py
```

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

## Alpha Survey Runner
If you're looking for the Survey Runner code from the Alpha then it has been renamed to: alpha-eq-survey-runner
- https://github.com/ONSdigital/alpha-eq-survey-runner
