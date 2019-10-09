from pytest import fixture

from app.setup import create_app


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


@fixture
def app():
    setting_overrides = {'LOGIN_DISABLED': True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app

