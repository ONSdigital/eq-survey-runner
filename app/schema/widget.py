import logging

from app.data_model.answer_store import AnswerStore

logger = logging.getLogger(__name__)


class Widget(object):
    def __init__(self, name):
        self.name = name

    def render(self, state):
        raise NotImplementedError

    def get_user_input(self, post_vars):
        if isinstance(post_vars, AnswerStore):
            return None

        user_input = post_vars.get(self.name, None)
        logger.debug('Getting user input for "{}", value is "{}"'.format(self.name, user_input))
        return user_input

    def get_other_input(self, post_vars):
        pass
