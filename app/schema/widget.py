from structlog import get_logger

logger = get_logger()


class Widget(object):
    def __init__(self, schema_item_id):
        self.id = schema_item_id
        self.name = schema_item_id

    def render(self, state):
        raise NotImplementedError

    def get_user_input(self, post_vars):
        user_input = post_vars.get(self.name, None)
        logger.debug('getting user input', input_name=self.name)
        return user_input

    def get_other_input(self, post_vars, options):
        pass
