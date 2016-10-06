import logging


logger = logging.getLogger(__name__)


class Widget(object):
    def __init__(self, name):
        self.name = name

    def render(self, state):
        raise NotImplementedError

    def get_user_input(self, post_vars):
        user_input = post_vars.get(self.name, None)
        logger.debug('Getting user input for "{}", value is "{}"'.format(self.name, user_input))
        return user_input

    def get_other_input(self, post_vars):
        list_of_values = post_vars.getlist(self.name)
        if not list_of_values:
            return None
        logger.debug('There are {} entries in the list: {}'.format(len(list_of_values), list_of_values))
        user_input = list_of_values[-1:][0]
        logger.debug('Getting user input for "{}", value is "{}"'.format(self.name, user_input))
        return user_input
