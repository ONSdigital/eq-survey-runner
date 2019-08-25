import pytest
from mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.setup import create_app


@pytest.fixture
def app():
    setting_overrides = {'LOGIN_DISABLED': True}
    app = create_app(setting_overrides=setting_overrides)

    return app


@pytest.fixture
def people_answer_store():
    return AnswerStore(
        [
            {'answer_id': 'first-name', 'value': 'Toni', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'last-name', 'value': 'Morrison', 'list_item_id': 'PlwgoG'},
            {'answer_id': 'first-name', 'value': 'Barry', 'list_item_id': 'UHPLbX'},
            {'answer_id': 'last-name', 'value': 'Pheloung', 'list_item_id': 'UHPLbX'},
        ]
    )


@pytest.fixture
def people_list_store():
    return ListStore([{'items': ['PlwgoG', 'UHPLbX'], 'name': 'people'}])
