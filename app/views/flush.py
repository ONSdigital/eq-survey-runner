from flask import Blueprint, Response, request, session

from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.user import User
from app.authentication.user_id_generator import UserIDGenerator
from app.globals import get_answer_store, get_metadata, get_questionnaire_store
from app.questionnaire.path_finder import PathFinder
from app.submitter.converter import convert_answers
from app.submitter.submitter import SubmitterFactory
from app.utilities.schema import load_schema_from_metadata

flush_blueprint = Blueprint('flush', __name__)


@flush_blueprint.route('/flush', methods=['GET'])
def flush_data():

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if encrypted_token is None:
        return Response(status=403)

    decoder = JWTDecryptor()
    decrypted_token = decoder.decrypt_jwt_token(encrypted_token)

    roles = decrypted_token.get('roles')

    if roles and 'flusher' in roles:
        user = _get_user(decrypted_token)
        if _submit_data(user):
            return Response(status=200)
        else:
            return Response(status=404)
    else:
        return Response(status=403)


def _submit_data(user):

    answer_store = get_answer_store(user)

    if answer_store.answers:
        metadata = get_metadata(user)
        schema = load_schema_from_metadata(metadata)
        routing_path = PathFinder(schema, answer_store, metadata).get_routing_path()
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, schema, answer_store, routing_path)
        submitter.send_answers(message)
        get_questionnaire_store(user.user_id, user.user_ik).delete()
        return True
    else:
        return False


def _get_user(decrypted_token):
    user_id = UserIDGenerator.generate_id(decrypted_token)
    user_ik = UserIDGenerator.generate_ik(decrypted_token)
    return User(user_id, user_ik)
