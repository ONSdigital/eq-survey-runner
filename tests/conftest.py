import pytest
import mock
import os
from app import create_app
from config import configs
from app import settings


@pytest.fixture(scope='session')
def survey_runner(request):
    with open(os.getcwd() + '/jwt-test-keys/rrm-public.pem', "rb") as public_key_file:
        settings.EQ_RRM_PUBLIC_KEY = public_key_file.read()
    with open(os.getcwd() + '/jwt-test-keys/sr-private.pem', "rb") as private_key_file:
        settings.EQ_SR_PRIVATE_KEY = private_key_file.read()

    print("setting up survey runner")
    app = create_app('test')
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def survey_runner_config(survey_runner):
    survey_runner.config['SR_ENVIRONMENT'] = 'test'
    survey_runner.config.from_object(configs['test'])


@pytest.fixture
def os_environ(request):
    env_patch = mock.patch('os.environ', {})
    request.addfinalizer(env_patch.stop)

    return env_patch.start()
