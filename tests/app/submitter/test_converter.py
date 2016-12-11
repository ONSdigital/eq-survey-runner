import dateutil.parser

from datetime import datetime, timedelta, timezone

from app.data_model.answer_store import AnswerStore
from app.parser.metadata_parser import parse_metadata
from app.schema.answer import Answer
from app.schema.block import Block
from app.schema.group import Group
from app.schema.question import Question
from app.schema.questionnaire import Questionnaire
from app.schema.section import Section
from app.submitter.converter import convert_answers, DataVersionError
from tests.app.framework.sr_unittest import SurveyRunnerTestCase

metadata = parse_metadata({
  "user_id": "789473423",
  "form_type": "0205",
  "collection_exercise_sid": "test-sid",
  "eq_id": "1",
  "period_id": "2016-02-01",
  "period_str": "2016-01-01",
  "ref_p_start_date": "2016-02-02",
  "ref_p_end_date": "2016-03-03",
  "ru_ref": "432423423423",
  "ru_name": "Apple",
  "return_by": "2016-07-07"
})


class TestConverter(SurveyRunnerTestCase):
    def test_convert_answers(self):
        with self.application.test_request_context():
            user_answer = [create_answer('ABC', '2016-01-01'), create_answer('DEF', '2016-03-30')]

            answer_1 = Answer()
            answer_1.id = "ABC"
            answer_1.code = "001"

            answer_2 = Answer()
            answer_2.id = "DEF"
            answer_2.code = "002"

            question = Question()
            question.id = 'question-1'
            question.add_answer(answer_1)
            question.add_answer(answer_2)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.data_version = "0.0.1"
            questionnaire.add_group(group)

            questionnaire.register(group)
            questionnaire.register(block)
            questionnaire.register(section)
            questionnaire.register(question)
            questionnaire.register(answer_1)
            questionnaire.register(answer_2)

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})

            self.assertEqual(answer_object['type'], 'uk.gov.ons.edc.eq:surveyresponse')
            self.assertEqual(answer_object['version'], '0.0.1')
            self.assertEqual(answer_object['origin'], 'uk.gov.ons.edc.eq')
            self.assertEqual(answer_object['survey_id'], '021')
            self.assertEqual(answer_object['collection']['exercise_sid'], metadata['collection_exercise_sid'])
            self.assertEqual(answer_object['collection']['instrument_id'], metadata['form_type'])
            self.assertEqual(answer_object['collection']['period'], metadata['period_id'])
            self.assertEqual(answer_object['metadata']['user_id'], metadata['user_id'])
            self.assertEqual(answer_object['metadata']['ru_ref'], metadata['ru_ref'])
            self.assertEqual(answer_object['data']['001'], '2016-01-01')
            self.assertEqual(answer_object['data']['002'], '2016-03-30')

    def test_submitted_at_should_be_set_in_payload(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0)]
            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.data_version = '0.0.2'

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})

            self.assertLess(datetime.now(timezone.utc) - dateutil.parser.parse(answer_object['submitted_at']), timedelta(seconds=5))

    def test_answer_with_zero(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0)]

            answer = Answer()
            answer.id = "GHI"
            answer.code = "003"

            question = Question()
            question.id = 'question-2'
            question.add_answer(answer)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.data_version = "0.0.1"
            questionnaire.add_group(group)
            questionnaire.register(question)
            questionnaire.register(answer)

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})

            # Check the converter correctly
            self.assertEquals("0", answer_object["data"]["003"])

    def test_answer_with_multiple_instances(self):
        with self.application.test_request_context():
            user_answer = [create_answer('GHI', 0),
                           create_answer('GHI', value=1, answer_instance=1),
                           create_answer('GHI', value=2, answer_instance=2)]

            answer = Answer()
            answer.id = "GHI"
            answer.code = "003"

            question = Question()
            question.id = 'question-2'
            question.add_answer(answer)

            section = Section()
            section.add_question(question)

            block = Block()
            block.id = 'block-1'
            block.add_section(section)

            group = Group()
            group.id = 'group-1'
            group.add_block(block)

            questionnaire = Questionnaire()
            questionnaire.survey_id = "021"
            questionnaire.data_version = "0.0.1"
            questionnaire.add_group(group)
            questionnaire.register(question)
            questionnaire.register(answer)

            answer_object = convert_answers(metadata, questionnaire, AnswerStore(user_answer), {})
            # Check the converter correctly
            self.assertEqual(answer_object["data"]["003"], ['0', '1', '2'])

    def test_convert_census_answers(self):
        with self.application.test_request_context():
            routing_path = [location(group_id='personal details', block_id='about you'),
                            location(group_id='household', block_id='where you live'),
                            location(group_id='household', block_id='where you live', group_instance=1)]
            answers = [create_answer('name', 'Joe Bloggs', group_id='personal details', block_id='about you'),
                       create_answer('name', 'Fred Bloggs', group_id='personal details', block_id='about you', answer_instance=1),
                       create_answer('address', '62 Somewhere', group_id='household', block_id='where you live'),
                       create_answer('address', '63 Somewhere', group_id='household', block_id='where you live', group_instance=1)]
            questionnaire = Questionnaire()
            questionnaire.survey_id = '021'
            questionnaire.data_version = '0.0.2'

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 4)
            self.assertEqual(answer_object['data'][0]['group_id'], 'personal details')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['block_id'], 'about you')
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], 'Joe Bloggs')
            self.assertEqual(answer_object['data'][1]['group_id'], 'personal details')
            self.assertEqual(answer_object['data'][1]['group_instance'], 0)
            self.assertEqual(answer_object['data'][1]['block_id'], 'about you')
            self.assertEqual(answer_object['data'][1]['answer_instance'], 1)
            self.assertEqual(answer_object['data'][1]['value'], 'Fred Bloggs')
            self.assertEqual(answer_object['data'][2]['group_id'], 'household')
            self.assertEqual(answer_object['data'][2]['group_instance'], 0)
            self.assertEqual(answer_object['data'][2]['block_id'], 'where you live')
            self.assertEqual(answer_object['data'][2]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][2]['value'], '62 Somewhere')
            self.assertEqual(answer_object['data'][3]['group_id'], 'household')
            self.assertEqual(answer_object['data'][3]['group_instance'], 1)
            self.assertEqual(answer_object['data'][3]['block_id'], 'where you live')
            self.assertEqual(answer_object['data'][3]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][3]['value'], '63 Somewhere')

    def test_convert_census_answers_multiple_answers(self):
        with self.application.test_request_context():
            routing_path = [location(group_id='favourite food', block_id='crisps')]
            answers = [create_answer('name', ['Ready salted', 'Sweet chilli'], group_id='favourite food', block_id='crisps')]
            questionnaire = Questionnaire()
            questionnaire.survey_id = '021'
            questionnaire.data_version = '0.0.2'

            # When
            answer_object = convert_answers(metadata, questionnaire, AnswerStore(answers), routing_path)

            # Then
            self.assertEqual(len(answer_object['data']), 1)
            self.assertEqual(answer_object['data'][0]['group_id'], 'favourite food')
            self.assertEqual(answer_object['data'][0]['group_instance'], 0)
            self.assertEqual(answer_object['data'][0]['block_id'], 'crisps')
            self.assertEqual(answer_object['data'][0]['answer_instance'], 0)
            self.assertEqual(answer_object['data'][0]['value'], ['Ready salted', 'Sweet chilli'])

    def test_converter_raises_runtime_error_for_unsupported_version(self):
        with self.application.test_request_context():
            questionnaire = Questionnaire()
            questionnaire.survey_id = '021'
            questionnaire.data_version = '-0.0.1'

            with self.assertRaises(DataVersionError) as err:
                convert_answers(metadata, questionnaire, AnswerStore(), {})

            self.assertEqual(str(err.exception), 'Data version -0.0.1 not supported')


def create_answer(answer_id, value, group_id=None, block_id=None, answer_instance=0, group_instance=0):
    return {
        'group_id': group_id,
        'block_id': block_id,
        'answer_id': answer_id,
        'answer_instance': answer_instance,
        'group_instance': group_instance,
        'value': value,
    }


def location(group_id, block_id, group_instance=0):
    return {
        'group_id': group_id,
        'block_id': block_id,
        'group_instance': group_instance
    }
