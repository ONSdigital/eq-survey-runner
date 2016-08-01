from app.questionnaire_state.user_journey_manager import UserJourneyManager
import logging

logger = logging.getLogger(__name__)


class RoutingException(Exception):
    pass


class RoutingEngine(object):
    ''' The routing engine will apply any routing rules dependant on where the user is in the schema
    and what answers they have provided.
    '''
    def __init__(self, schema_model):
        self._schema = schema_model

    def get_next_location(self, current_location):
        if current_location == 'introduction':
            next_location = self._schema.groups[0].blocks[0].id
        elif current_location == 'summary':
            next_location = 'thank-you'
        else:
            current_block = self._schema.get_item_by_id(current_location)
            if current_block:
                current_group = current_block.container

                # Check if there are any routing rules
                routing_rules = current_block.routing_rules
                if routing_rules:
                    return self._process_routing_rules(routing_rules)
                else:
                    next_location = self._basic_routing(current_group, current_block)
            else:
                raise RoutingException('Cannot route: No current block')
        return next_location

    def get_first_block(self):
        return self._schema.groups[0].blocks[0].id

    def _basic_routing(self, current_group, current_block):
        # function for linear routing, i.e it goes to the next block in the JSON
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
        return 'summary'

    @staticmethod
    def _process_routing_rules(routing_rules):

        logger.debug("Processing routing rules %s", routing_rules)
        user_journey_manager = UserJourneyManager.get_instance()

        try:
            for rule in routing_rules:
                goto_id = rule['goto']['id']

                # If there isn't a 'when' we just go straight to the id
                if 'when' not in rule['goto'].keys():
                    return goto_id
                else:

                    when = rule['goto']['when']
                    match_value = when['value']
                    condition = when['condition']
                    user_answer = user_journey_manager.get_answer(when['id'])

                    # Evaluate the condition on the routing rule
                    if condition == 'equals':
                        if match_value == user_answer:
                            return goto_id
                    if condition == 'not equals':
                        if match_value != user_answer:
                            return goto_id

        except:
            logger.error("Routing rules error")
            raise RoutingException('Cannot route: Routing rule not configured correctly')
