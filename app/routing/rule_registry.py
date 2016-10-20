from app.routing.routing_exception import RoutingException
from app.routing.rules.goto_block_rule import GotoBlockRule


KNOWN_RULES = {
    'goto': GotoBlockRule,
}


class RuleRegistry(object):

    @staticmethod
    def get_rule(rule):
        for known_rule in KNOWN_RULES:
            if known_rule in rule:
                return KNOWN_RULES[known_rule]
        raise RoutingException('Rule {} not supported'.format(rule))
