from unittest.mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.views.handlers.section_summary import SectionSummary
from app.utilities.schema import load_schema_from_name
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from tests.app.views.handlers.test_summary_handler import TestStandardSummaryHandler


class TestSectionSummaryHandler(TestStandardSummaryHandler):
    def setUp(self):
        super().setUp()
        self.block_type = 'SectionSummary'
        self.language = 'en'
        self.current_location = Location(
            section_id='property-details-section', block_id='property-details-summary'
        )

        storage = MagicMock()
        storage.get_user_data = MagicMock(return_value=('{}', 1))
        storage.add_or_update = MagicMock()

        self.questionnaire_store = QuestionnaireStore(storage)
        self.questionnaire_store.answer_store = AnswerStore()
        self.questionnaire_store.progress_store = ProgressStore(
            [
                {
                    'section_id': 'property-details-section',
                    'list_item_id': None,
                    'status': CompletionStatus.COMPLETED,
                    'locations': [
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'insurance-type',
                        },
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'insurance-address',
                        },
                        {
                            'section_id': 'property-details-section',
                            'block_id': 'address-duration',
                        },
                    ],
                }
            ]
        )
        self.schema = load_schema_from_name('test_section_summary')

    def test_build_summary_rendering_context(self):
        summary = SectionSummary(
            self.schema,
            self.questionnaire_store,
            self.language,
            self.current_location,
            None,
        )
        context = summary.get_context()
        self.check_groups(context['summary']['groups'])
        self.assertTrue('title' in context['summary'])


def test_context_for_section_list_summary(people_answer_store, app):
    schema = load_schema_from_name('test_list_collector_section_summary')
    current_location = Location(
        block_id='people-list-section-summary', section_id='section'
    )

    storage = MagicMock()
    storage.get_user_data = MagicMock(return_value=('{}', 1))
    storage.add_or_update = MagicMock()

    questionnaire_store = QuestionnaireStore(storage)
    questionnaire_store.answer_store = people_answer_store
    questionnaire_store.list_store = ListStore(
        [
            {'items': ['PlwgoG', 'UHPLbX'], 'name': 'people'},
            {'items': ['gTrlio'], 'name': 'visitors'},
        ]
    )
    questionnaire_store.progress_store = ProgressStore(
        [
            {
                'section_id': 'section',
                'list_item_id': None,
                'status': CompletionStatus.COMPLETED,
                'locations': [
                    {
                        'section_id': 'section',
                        'block_id': 'primary-person-list-collector',
                    },
                    {'section_id': 'section', 'block_id': 'list-collector'},
                    {'section_id': 'section', 'block_id': 'visitor-list-collector'},
                ],
            }
        ]
    )

    summary = SectionSummary(
        schema, questionnaire_store, DEFAULT_LANGUAGE_CODE, current_location, None
    )

    context = summary.get_context()

    expected = [
        {
            'add_link': '/questionnaire/people/add-person/',
            'add_link_text': 'Add someone to this household',
            'empty_list_text': 'There are no householders',
            'list_items': [
                {
                    'edit_link': '/questionnaire/people/PlwgoG/edit-person/',
                    'item_title': 'Toni Morrison',
                    'primary_person': False,
                    'remove_link': '/questionnaire/people/PlwgoG/remove-person/',
                },
                {
                    'edit_link': '/questionnaire/people/UHPLbX/edit-person/',
                    'item_title': 'Barry Pheloung',
                    'primary_person': False,
                    'remove_link': '/questionnaire/people/UHPLbX/remove-person/',
                },
            ],
            'title': 'Household members on 13 October 2019',
            'list_name': 'people',
        },
        {
            'add_link': '/questionnaire/visitors/add-visitor/',
            'add_link_text': 'Add another visitor to this household',
            'empty_list_text': 'There are no visitors',
            'list_items': [
                {
                    'edit_link': '/questionnaire/visitors/gTrlio/edit-visitor-person/',
                    'item_title': '',
                    'primary_person': False,
                    'remove_link': '/questionnaire/visitors/gTrlio/remove-visitor/',
                }
            ],
            'title': 'Visitors staying overnight on 13 October 2019',
            'list_name': 'visitors',
        },
    ]

    assert context['summary']['list_summaries'] == expected
