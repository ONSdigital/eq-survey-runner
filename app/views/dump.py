from flask_login import current_user
from flask_login import login_required
from flask import Blueprint

import simplejson as json


from app.authentication.roles import role_required
from app.globals import get_questionnaire_store, get_session_store, get_answer_store
from app.submitter.converter import convert_answers
from app.utilities.schema import load_schema_from_session_data
from app.questionnaire.path_finder import PathFinder


dump_blueprint = Blueprint('dump', __name__)


@dump_blueprint.route('/dump/answers', methods=['GET'])
@login_required
@role_required('dumper')
def dump_answers():
    response = {'answers': get_answer_store(current_user).serialise() or []}
    return json.dumps(response, for_json=True), 200


@dump_blueprint.route('/dump/submission', methods=['GET'])
@login_required
@role_required('dumper')
def dump_submission():
    questionnaire_store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
    answer_store = questionnaire_store.answer_store
    metadata = questionnaire_store.metadata
    session_data = get_session_store().session_data
    schema = load_schema_from_session_data(session_data)
    completed_blocks = questionnaire_store.completed_blocks
    routing_path = PathFinder(schema, answer_store, metadata, completed_blocks).get_full_routing_path()
    response = {'submission': convert_answers(schema, questionnaire_store, routing_path)}
    return json.dumps(response, for_json=True), 200
