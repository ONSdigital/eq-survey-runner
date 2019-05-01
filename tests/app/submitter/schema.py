from app.questionnaire.questionnaire_schema import QuestionnaireSchema, DEFAULT_LANGUAGE_CODE
from app.utilities.schema import _load_schema_file


def make_schema(data_version, section, group, block, question):
    return {
        'survey_id': '021',
        'data_version': data_version,
        'sections': [
            {
                'id': section,
                'groups': [
                    {
                        'id': group,
                        'blocks': [
                            {
                                'id': block,
                                'type': 'Question',
                                'question': question
                            }
                        ]
                    }
                ]
            }
        ]
    }


def load_schema(eq_id, form_type, language_code=None):
    language_code = language_code or DEFAULT_LANGUAGE_CODE
    schema_json = _load_schema_file('{}_{}.json'.format(eq_id, form_type), language_code)

    return QuestionnaireSchema(schema_json, language_code)
