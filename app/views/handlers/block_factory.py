from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.relationship_location import RelationshipLocation
from app.views.handlers.calculated_summary import CalculatedSummary
from app.views.handlers.content import Content
from app.views.handlers.list_add_question import ListAddQuestion
from app.views.handlers.list_collector import ListCollector
from app.views.handlers.list_edit_question import ListEditQuestion
from app.views.handlers.list_remove_question import ListRemoveQuestion
from app.views.handlers.primary_person_list_collector import PrimaryPersonListCollector
from app.views.handlers.primary_person_question import PrimaryPersonQuestion
from app.views.handlers.question import Question
from app.views.handlers.relationship_collector import RelationshipCollector
from app.views.handlers.section_summary import SectionSummary
from app.views.handlers.summary import Summary

BLOCK_MAPPINGS = {
    'Question': Question,
    'ConfirmationQuestion': Question,
    'ListCollector': ListCollector,
    'ListAddQuestion': ListAddQuestion,
    'ListEditQuestion': ListEditQuestion,
    'ListRemoveQuestion': ListRemoveQuestion,
    'PrimaryPersonListCollector': PrimaryPersonListCollector,
    'PrimaryPersonListAddOrEditQuestion': PrimaryPersonQuestion,
    'RelationshipCollector': RelationshipCollector,
    'Introduction': Content,
    'Interstitial': Content,
    'Confirmation': Content,
    'Summary': Summary,
    'SectionSummary': SectionSummary,
    'CalculatedSummary': CalculatedSummary,
}


def get_block_handler(
    schema,
    block_id,
    list_item_id,
    questionnaire_store,
    language,
    list_name=None,
    to_list_item_id=None,
    return_to=None,
):
    block = schema.get_block(block_id)
    if not block:
        raise InvalidLocationException(
            f'block id {block_id} is not valid for this schema'
        )

    if schema.is_block_in_repeating_section(block_id=block['id']) and not all(
        (list_name, list_item_id)
    ):
        raise InvalidLocationException(
            f'block id {block_id} is in a repeating section without valid list_name/list_item_id'
        )

    block_type = block['type']
    block_class = BLOCK_MAPPINGS.get(block_type)
    if not block_class:
        raise ValueError(f'block type {block_type} is not valid')

    section_id = schema.get_section_id_for_block_id(block_id)

    if to_list_item_id:
        location = RelationshipLocation(
            section_id=section_id,
            block_id=block_id,
            list_item_id=list_item_id,
            to_list_item_id=to_list_item_id,
        )
    else:
        location = Location(
            section_id=section_id,
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
        )

    return block_class(schema, questionnaire_store, language, location, return_to)
