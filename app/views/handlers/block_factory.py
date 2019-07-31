from app.views.handlers.content import Content
from app.views.handlers.question import Question
from app.views.handlers.list_collector import ListCollector
from app.views.handlers.list_add_question import ListAddQuestion
from app.views.handlers.list_edit_question import ListEditQuestion
from app.views.handlers.list_remove_question import ListRemoveQuestion
from app.views.handlers.primary_person_list_collector import PrimaryPersonListCollector
from app.views.handlers.primary_person_question import PrimaryPersonQuestion
from app.views.handlers.relationship_collector import RelationshipCollector
from app.views.handlers.summary import Summary
from app.views.handlers.section_summary import SectionSummary
from app.views.handlers.calculated_summary import CalculatedSummary
from app.questionnaire.location import InvalidLocationException

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


def get_block_handler(schema, location, questionnaire_store, language):
    block = schema.get_block(location.block_id)
    if not block:
        raise InvalidLocationException(
            f'block id {location.block_id} is not valid for this schema'
        )

    block_type = block['type']
    block_class = BLOCK_MAPPINGS.get(block_type)
    if not block_class:
        raise ValueError(f'block type {block_type} is not valid')

    return block_class(schema, questionnaire_store, language, location)
