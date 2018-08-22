from collections import defaultdict


class GroupDependencies:
    """represents the dependencies for a group or groups
    held internally as a dict(string,list)

    group_drivers - list of groups driving a group dependency
    block_drivers - list of blocks with answers driving a group dependency

    To add a dependency either call add with a single dependency
    or update with another dependency object

    To access dependencies for a question id simply index
    i.e  a['group_id']
    indexing is read only
    """

    def __init__(self):
        self._group_dependencies = defaultdict(list)
        self._group_dependencies['group_drivers'] = []
        self._group_dependencies['block_drivers'] = []

    def __len__(self):
        """
        returns length of group dependencies, needed for index access
        -2 refers to the group and block drivers
        """

        return len(self._group_dependencies) - 2

    def __getitem__(self, group_id):
        """allows the support of indexing e.g a[group_id]"""
        return self._group_dependencies[group_id]

    @property
    def group_dependencies(self):
        return self._group_dependencies

    def add(self, dependent_id, dependency_driver_id, group_or_block):
        """ Adds a dependency to a specific group_id without duplicating """
        if dependency_driver_id not in self._group_dependencies[dependent_id]:
            self._group_dependencies[dependent_id].append(dependency_driver_id)
        if group_or_block == 'block' and dependency_driver_id not in self._group_dependencies['block_drivers']:
            self._group_dependencies['block_drivers'].append(dependency_driver_id)
        if group_or_block == 'group' and dependency_driver_id not in self._group_dependencies['group_drivers']:
            self._group_dependencies['group_drivers'].append(dependency_driver_id)

    def update(self, dependencies):
        for dependency in dependencies.group_dependencies:
            if dependency not in ['group_drivers', 'block_drivers']:
                for driver_id in dependencies[dependency]:
                    group_or_block = 'group' if driver_id in dependencies['group_drivers'] else 'block'
                    self.add(dependency, driver_id, group_or_block)


def get_group_dependencies(schema):
    """
    gets the all the answer dependencies for a schema by walking through repeats
    """
    dependencies = GroupDependencies()

    for group in schema.groups:
        if group.get('routing_rules') and not _group_has_relationship_type(schema, group['blocks']):
            for routing_rule in group['routing_rules']:
                if _routing_rule_has_repeat(routing_rule):
                    if 'group_ids' in routing_rule['repeat']:
                        dependencies.update(
                            _get_dependency_drivers_from_group_ids(group['id'],
                                                                   routing_rule['repeat']['group_ids']))
                    else:
                        dependencies.update(
                            _get_dependency_driver_from_answer_id(schema,
                                                                  group['id'],
                                                                  routing_rule['repeat']['answer_id']))

    return dependencies


def _get_dependency_drivers_from_group_ids(dependent_group_id, group_ids):
    dependencies = GroupDependencies()
    for group_id in group_ids:
        dependencies.add(dependent_group_id, group_id, 'group')

    return dependencies


def _get_dependency_driver_from_answer_id(schema, dependent_group_id, answer_id):
    dependencies = GroupDependencies()
    question_id = schema.get_answer(answer_id)['parent_id']
    block_id = schema.get_question(question_id)['parent_id']
    dependencies.add(dependent_group_id, block_id, 'block')

    return dependencies


def _group_has_relationship_type(schema, blocks):
    for block in blocks:
        if schema.block_has_question_type(block['id'], 'Relationship'):
            return True

    return False


def _routing_rule_has_repeat(routing_rule):
    dependent_routing_types = ['group', 'answer_count', 'answer_count_minus_one']
    if routing_rule.get('repeat') and routing_rule['repeat'].get('type') in dependent_routing_types:
        return True
    return False
