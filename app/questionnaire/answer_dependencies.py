from collections import defaultdict


class AnswerDependencies:
    """represents the dependencies for a group of answers
    held internally as a dict(string,set) where set contains dependent ids
    set used to prevent duplicates

    To add a dependency either call add with a single dependency
    or update with another dependency object

    To access dependencies for a question id simply index
    i.e  a['question_id']
    indexing is read only
    """
    def __init__(self):
        self._answer_dependencies = defaultdict(set)

    def __len__(self):
        """returns length of answer dependencies, needed for index access"""
        return len(self._answer_dependencies)

    def __getitem__(self, answer_id):
        """allows the support of indexing e.g a[answer_id]"""
        return self._answer_dependencies[answer_id]

    @property
    def answer_dependencies(self):
        return self._answer_dependencies

    def add(self, answer_id, dependency):
        """ Adds a dependency to a specific answer_id """
        self._answer_dependencies[answer_id].add(dependency)

    def update(self, other):
        for key, dependencies in other.answer_dependencies.items():
            self.answer_dependencies[key] |= dependencies


def get_answer_dependencies(schema):
    """gets the all the answer dependencies for a schema by walking questions and answers
    """
    dependencies = _get_answer_level_dependencies(schema)
    dependencies.update(_get_question_level_dependencies(schema))
    return dependencies


def _get_answer_level_dependencies(schema):
    # Answer level dependencies
    dependencies = AnswerDependencies()
    for answer in schema.answers:
        dependency_id = answer['id']
        if 'min_value' in answer and 'answer_id' in answer['min_value']:
            answer_id = answer['min_value']['answer_id']
            dependencies.add(answer_id, dependency_id)
        if 'max_value' in answer and 'answer_id' in answer['max_value']:
            answer_id = answer['max_value']['answer_id']
            dependencies.add(answer_id, dependency_id)
    return dependencies


def _get_question_level_dependencies(schema):
    # Question level dependencies
    dependencies = AnswerDependencies()
    for question in schema.questions:
        dependencies.update(_get_titles_dependencies_for_question(schema, question))
        for calculation in question.get('calculations', []):
            answer_id = calculation.get('answer_id')
            if answer_id:
                for dependency_id in calculation['answers_to_calculate']:
                    dependencies[answer_id].add(dependency_id)
    return dependencies


def _get_titles_dependencies_for_question(schema, question):
    """
    gets the unique ids of any answers on a question as dependents
    of any when id associated with a questions titles

    :param schema: the json schema to use
    :param question: the id of a question
    """
    dependencies = AnswerDependencies()

    answer_ids = schema.get_answer_ids_for_question(question['id'])

    when_clauses = [title.get('when')[0] for title in question.get('titles', []) if title.get('when')]

    for when_clause in when_clauses:
        when_id = when_clause.get('id')
        for answer_id in answer_ids:
            dependencies.add(when_id, answer_id)

    return dependencies
