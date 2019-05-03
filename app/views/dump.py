from flask_login import current_user
from flask_login import login_required
from quart import Blueprint, jsonify


from app.authentication.roles import role_required
from app.globals import (get_answer_store_async, get_metadata_async, get_completed_blocks_async, get_session_store_async,
                         get_collection_metadata_async)
from app.submitter.converter import convert_answers
from app.utilities.schema import load_schema_from_session_data
from app.questionnaire.path_finder import PathFinder


dump_blueprint = Blueprint('dump', __name__)


@dump_blueprint.route('/dump/answers', methods=['GET'])
@login_required
@role_required('dumper')
async def dump_answers():
    response = {'answers': list(await get_answer_store_async(current_user)) or []}
    return jsonify(response), 200


@dump_blueprint.route('/dump/submission', methods=['GET'])
@login_required
@role_required('dumper')
async def dump_submission():
    answer_store = await get_answer_store_async(current_user)
    metadata = await get_metadata_async(current_user)
    collection_metadata = await get_collection_metadata_async(current_user)
    session_data = (await get_session_store_async()).session_data
    schema = load_schema_from_session_data(session_data)
    completed_blocks = await get_completed_blocks_async(current_user)
    routing_path = PathFinder(schema, answer_store, metadata, completed_blocks).get_full_routing_path()
    response = {'submission': convert_answers(metadata, collection_metadata, schema, answer_store, routing_path)}
    return jsonify(response), 200
