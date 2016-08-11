from app.routing.routing_exception import RoutingException
from app.routing.rules.goto_block_rule import GotoBlockRule
from app.routing.rules.repeating_element_rule import RepeatingElementRule

KNOWN_RULES = {
    'goto': GotoBlockRule,
    'repeat': RepeatingElementRule,
}


class RuleRegistry(object):

    @staticmethod
    def get_rule(rule):
        for known_rule in KNOWN_RULES:
            if known_rule in rule:
                return KNOWN_RULES[known_rule]
        raise RoutingException('Rule {} not supported'.format(rule))
