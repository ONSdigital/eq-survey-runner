# pylint: disable=redefined-outer-name
import pytest
from app.templating.metadata_context import build_metadata_context_for_survey_completed
from app.data_model.session_data import SessionData


@pytest.fixture
def fake_session_data():
    return SessionData(
        tx_id='tx_id',
        eq_id='eq_id',
        form_type='form_type',
        language_code=None,
        survey_url=None,
        ru_ref='ru_ref',
        response_id='response_id',
        case_id='case_id',
        period_str=None,
        ru_name=None,
    )


def test_context_includes_period_str_if_available(fake_session_data):
    fake_session_data.period_str = 'some name'

    context = build_metadata_context_for_survey_completed(fake_session_data)

    assert context['period_str'] == 'some name'


def test_context_includes_ru_name_if_available(fake_session_data):
    fake_session_data.ru_name = 'some name'

    context = build_metadata_context_for_survey_completed(fake_session_data)

    assert context['ru_name'] == 'some name'


def test_context_does_not_include_period_str_and_ru_name_by_default(fake_session_data):
    context = build_metadata_context_for_survey_completed(fake_session_data)
    assert 'ru_name' not in context
    assert 'period_str' not in context
