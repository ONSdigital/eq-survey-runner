

class UserAction(object):
    '''
    Using the chain of responsibility pattern hand off a user action down the chain
    until one of the objects can handle it
    '''
    def __init__(self, schema):
        self._schema = schema
        self.next_action = None

    def set_next_action(self, action):
        self.next_action = action
        return action

    def process_action(self, action, current_location):
        if action == self.get_action():
            return self.provide_next_location(current_location)
        else:
            return self.next_action.process_action(action, current_location)

    def get_action(self):
        pass

    def provide_next_location(self, current_location):
        pass


class StartQuestionnaire(UserAction):
    def get_action(self):
        return 'start_questionnaire'

    def provide_next_location(self, current_location):
        return self._schema.groups[0].blocks[0].id


class SaveContinue(UserAction):
    def get_action(self):
        return 'save_continue'

    def provide_next_location(self, current_location):
        # We have already been validated so we only
        # need to figure out where to go next
        next_location = current_location
        current_block = self._schema.get_item_by_id(current_location)
        if current_block:
            current_group = current_block.container

            for index, block in enumerate(current_group.blocks):
                if block.id == current_block.id:
                    if index + 1 < len(current_group.blocks):
                        # return the next block in this group
                        return current_group.blocks[index + 1].id

            for index, group in enumerate(self._schema.groups):
                if group.id == current_group.id:
                    if index + 1 < len(self._schema.groups):
                        # return the first block in the next group
                        return self._schema.groups[index + 1].blocks[0].id

            # There are no more blocks or groups, go to summary
            next_location = 'summary'
            return next_location
        else:
            raise RoutingException('Cannot route: No current block')


class SubmitAnswers(UserAction):
    def get_action(self):
        return 'submit_answers'

    def provide_next_location(self, current_location):
        return 'thank-you'


class RoutingException(Exception):
    pass


class RoutingEngine(object):
    def __init__(self, schema_model):
        self._schema = schema_model
        self.route = self._build_routing_rules()

    def _build_routing_rules(self):
        # build the chain of responsibility
        start_questionnaire = StartQuestionnaire(self._schema)
        save_continue = SaveContinue(self._schema)
        submit = SubmitAnswers(self._schema)
        start_questionnaire.set_next_action(save_continue).set_next_action(submit)
        return start_questionnaire

    def get_next(self, current_location, user_action):
        return self.route.process_action(user_action, current_location)
