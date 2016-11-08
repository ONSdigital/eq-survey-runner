import json
import os
import unittest
from unittest import mock

import datetime

from mock import Mock, patch

from app import settings
from app.questionnaire_state.state_block import StateBlock
from app.templating.model_builder import build_summary_model, build_questionnaire_model
from tests.app.templating.summary.test_section import build_block_schema


class TestBuildModel(unittest.TestCase):

    metadata = {'return_by': '2016-10-10',
                'ref_p_start_date': '2016-10-10',
                'ref_p_end_date': '2016-10-10',
                'ru_ref': 'abc123',
                'ru_name': 'Mr Bloggs',
                'trad_as': 'Apple',
                'tx_id': '12345678-1234-5678-1234-567812345678',
                'period_str': '201610',
                'employment_date': '2016-10-10',
                }

    def setUp(self):
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, "0_star_wars.json"))
        schema = schema_file.read()
        # create a parser
        self.schema_json = json.loads(schema)

    def test_build_summary_model(self):
        with patch('app.templating.metadata_template_preprocessor.get_metadata', return_value=TestBuildModel.metadata), \
                patch('app.templating.model_builder.get_answers', return_value=Mock(return_value={})), \
                patch('app.templating.model_builder.g', return_value=mock.MagicMock()), \
                patch('app.templating.metadata_template_preprocessor.to_date', return_value=datetime.datetime.now()):
            render_data = build_summary_model(self.schema_json)

        self.assertIsNotNone(render_data['content'])
        self.assertIsNotNone(render_data['meta'])

    def test_build_summary_model_sections(self):
        with patch('app.templating.metadata_template_preprocessor.get_metadata', return_value=TestBuildModel.metadata), \
                patch('app.templating.model_builder.get_answers', return_value=Mock(return_value={'ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c': 'Light Side'})), \
                patch('app.templating.model_builder.g') as mock_g, \
                patch('app.templating.metadata_template_preprocessor.to_date', return_value=datetime.datetime.now()):
            mock_g.questionnaire_manager.navigator.get_routing_path = Mock(return_value={'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0'})
            render_data = build_summary_model(self.schema_json)

        self.assertIsNotNone(render_data['content'])
        self.assertEqual(len(render_data['content']), 1)
        self.assertEqual(render_data['content'][0].title, 'Choose your side')

    def test_create_sections_shows_answers_for_final_path(self):
        # Given
        first_answer_schema = {'id': '1', 'type': 'text', 'label': ''}
        second_answer_schema = {}
        first_block = build_block_schema(first_answer_schema, '1')
        second_block = build_block_schema(second_answer_schema, '2')
        group = {'blocks': [first_block, second_block]}
        schema = {'groups': [group], 'introduction': {}, 'title': '', 'theme': '', 'survey_id': ''}

        # When
        with patch('app.templating.metadata_template_preprocessor.get_metadata', return_value=TestBuildModel.metadata), \
                patch('app.templating.model_builder.get_answers', return_value=Mock(return_value={'1': 'For answer 1'})), \
                patch('app.templating.model_builder.g') as mock_g:
            mock_g.questionnaire_manager.navigator.get_routing_path = Mock(return_value=['1'])
            summary = build_summary_model(schema)

        # Then
        self.assertEqual(len(summary['content']), 1)
        self.assertEqual(summary['content'][0].id, 'section1')

    def test_build_questionnaire_model(self):
        state_item = StateBlock("1", None)

        with patch('app.templating.metadata_template_preprocessor.get_metadata', return_value=TestBuildModel.metadata), \
                patch('app.templating.metadata_template_preprocessor.to_date', return_value=datetime.datetime.now()):
            render_data = build_questionnaire_model(self.schema_json, state_item)

        self.assertIsNotNone(render_data)
        self.assertEqual(state_item, render_data['content'])

        self.assertIsNotNone(render_data['meta'])
