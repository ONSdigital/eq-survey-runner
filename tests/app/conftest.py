from pytest import fixture

from app.setup import create_app


@fixture
def app():
    setting_overrides = {'LOGIN_DISABLED': True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app
