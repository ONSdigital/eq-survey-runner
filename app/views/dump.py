from flask_login import current_user
from flask_login import login_required
from flask import Blueprint, jsonify


from app.authentication.roles import role_required
from app.globals import get_answer_store, get_metadata, get_completed_blocks
from app.submitter.converter import convert_answers
from app.utilities.schema import load_schema_from_metadata
from app.questionnaire.path_finder import PathFinder


dump_blueprint = Blueprint('dump', __name__)


@dump_blueprint.route('/dump/answers', methods=['GET'])
@login_required
@role_required('dumper')
def dump_answers():
    response = {'answers': get_answer_store(current_user).answers or []}
    return jsonify(response), 200


@dump_blueprint.route('/dump/submission', methods=['GET'])
@login_required
@role_required('dumper')
def dump_submission():
    answer_store = get_answer_store(current_user)
    metadata = get_metadata(current_user)
    schema = load_schema_from_metadata(metadata)
    completed_blocks = get_completed_blocks(current_user)
    routing_path = PathFinder(schema, answer_store, metadata, completed_blocks).get_full_routing_path()
    response = {'submission': convert_answers(metadata, schema, answer_store, routing_path)}
    return jsonify(response), 200
