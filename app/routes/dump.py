from functools import wraps

from flask import Blueprint
from flask import g
from flask_login import current_user
from flask_login import login_required
import simplejson as json

from app.authentication.roles import role_required
from app.globals import get_questionnaire_store, get_session_store
from app.helpers.path_finder_helper import path_finder
from app.submitter.converter import convert_answers
from app.utilities.schema import load_schema_from_session_data


dump_blueprint = Blueprint('dump', __name__)


def requires_schema(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = get_session_store()
        g.schema = load_schema_from_session_data(session.session_data)
        result = func(g.schema, *args, **kwargs)
        return result

    return wrapper


@dump_blueprint.route('/dump/debug', methods=['GET'])
@login_required
@role_required('dumper')
def dump_debug():
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    return questionnaire_store.serialise()


@dump_blueprint.route('/dump/routing-path', methods=['GET'])
@login_required
@role_required('dumper')
@requires_schema
def dump_routing(schema):  # pylint: disable=unused-argument
    response = {'routing_path': path_finder.full_routing_path()}
    return json.dumps(response, for_json=True), 200


@dump_blueprint.route('/dump/submission', methods=['GET'])
@login_required
@role_required('dumper')
@requires_schema
def dump_submission(schema):
    routing_path = path_finder.full_routing_path()
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    response = {
        'submission': convert_answers(schema, questionnaire_store, routing_path)
    }
    return json.dumps(response, for_json=True), 200
