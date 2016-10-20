import logging

from app.routing.routing_exception import RoutingException
from app.routing.rule_registry import RuleRegistry
logger = logging.getLogger(__name__)


class RoutingEngine(object):
    ''' The routing engine will apply any routing rules dependant on where the user is in the schema
    and what answers they have provided.
    '''
    def __init__(self, schema_model, questionnaire_manager):
        self._schema = schema_model
        self._questionnaire_manager = questionnaire_manager

    def get_next_location(self, current_location):
        if current_location == 'introduction':
            next_location = self._schema.groups[0].blocks[0].id
        elif current_location == self._schema.submission_page:
            next_location = 'thank-you'
        else:
            current_block = self._schema.get_item_by_id(current_location)
            if current_block:

                # Check if there are any routing rules
                routing_rules = current_block.routing_rules
                if routing_rules:
                    return self._process_routing_rules(routing_rules, current_block)
                else:
                    next_location = self._basic_routing(current_block)
            else:
                raise RoutingException('Cannot route: No current block')
        return next_location

    def get_first_block(self):
        return self._schema.groups[0].blocks[0].id

    def _basic_routing(self, current_block):
        # function for linear routing, i.e it goes to the next block in the JSON
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

        # There are no more blocks or groups, go to submission page (Default is summary)
        return self._schema.submission_page

    def _process_routing_rules(self, routing_rules, current_block):

        logger.debug("Processing routing rules %s", routing_rules)
        for rule in routing_rules:

            # Work out which rule we need then get it to work out the next location
            rule_class = RuleRegistry.get_rule(rule)
            next_location_rule = rule_class(self._questionnaire_manager, rule)
            next_location = next_location_rule.next_location()

            if next_location:
                return next_location

        return self._basic_routing(current_block)
