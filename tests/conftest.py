import mock
import pytest

from app import create_app
from app import settings
from config import configs
from tests.app.authentication import TEST_DO_NOT_USE_RRM_PUBLIC_PEM, TEST_DO_NOT_USE_SR_PRIVATE_PEM


@pytest.fixture(scope='session')
def survey_runner(request):
    settings.EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = TEST_DO_NOT_USE_RRM_PUBLIC_PEM
    settings.EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = TEST_DO_NOT_USE_SR_PRIVATE_PEM

    print("setting up survey runner")
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def survey_runner_config(_survey_runner):
    _survey_runner.config['SR_ENVIRONMENT'] = 'test'
    _survey_runner.config.from_object(configs['test'])


@pytest.fixture
def os_environ(request):
    env_patch = mock.patch('os.environ', {})
    request.addfinalizer(env_patch.stop)

    return env_patch.start()
