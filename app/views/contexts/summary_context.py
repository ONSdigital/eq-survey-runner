from typing import List, Mapping

from flask import url_for
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


def get_section_context(section, block_ids_to_filter) -> List:
    group_collection = []

    for group_schema in section['groups']:
        blocks_to_return = []
        for block in group_schema['blocks']:
            if block['id'] in block_ids_to_filter and block['type'] == 'Question':
                blocks_to_return.append(
                    {
                        'id': block['id'],
                        'title': block.get('title'),
                        'number': block.get('number'),
                        'link': url_for('questionnaire.block', block_id=block['id']),
                    }
                )
        group_collection.append(
            {
                'id': group_schema['id'],
                'title': group_schema.get('title'),
                'blocks': blocks_to_return,
            }
        )
    return group_collection


def build_group_summary_context(
    schema: QuestionnaireSchema, path_finder: PathFinder, sections: List[Mapping] = None
) -> List:
    sections = sections or schema.get_sections()
    paths = [path_finder.routing_path(section['id']) for section in sections]

    group_collection = []

    for path, section in zip(paths, sections):
        block_ids_on_path = [location.block_id for location in path]
        group_collection.extend(get_section_context(section, block_ids_on_path))
    return group_collection
