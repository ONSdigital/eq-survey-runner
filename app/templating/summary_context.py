from typing import List, Mapping

from app.data_model.answer_store import AnswerStore
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.templating.summary.group import Group


def build_summary_rendering_context(
    schema: QuestionnaireSchema,
    answer_store: AnswerStore,
    metadata: Mapping,
    sections: List[Mapping] = None,
) -> List:
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire.
    :param schema: schema of the current questionnaire
    :param answer_store: all of the answers to the questionnaire
    :param metadata: all of the metadata
    :return: questionnaire summary context
    """
    path_finder = PathFinder(schema, answer_store, metadata)

    sections = sections or schema.get_sections()
    paths = [path_finder.routing_path(section) for section in sections]

    return [
        Group(group, path, answer_store, metadata, schema).serialize()
        for path, section in zip(paths, sections)
        for group in section['groups']
    ]
