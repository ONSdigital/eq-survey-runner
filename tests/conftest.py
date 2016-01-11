import pytest
import mock
from app import create_app
from config import configs


@pytest.fixture(scope='session')
def survey_runner(request):
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
