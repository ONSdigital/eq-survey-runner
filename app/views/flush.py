from app.globals import get_answer_store, get_metadata, get_questionnaire_store
from app.submitter.submitter import SubmitterFactory
from app.submitter.converter import convert_answers
from app.utilities.schema import get_schema

from app.authentication.flush_permission_denied import FlushPermissionDenied
from app.authentication.jwt_decoder import JWTDecryptor
from app.authentication.map_role_to_permissions import map_role_to_permissions
from app.authentication.no_survey_data_to_flush import NoSurveyDataToFlush
from app.authentication.no_token_exception import NoTokenException
from app.authentication.user import User
from app.authentication.user_id_generator import UserIDGenerator

from app.questionnaire.path_finder import PathFinder

from flask import Blueprint, Response, request, session

flush_blueprint = Blueprint('flush', __name__)


@flush_blueprint.route('/flush', methods=['GET'])
def flush_data():

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if encrypted_token is None:
        raise NoTokenException("Please provide a token")

    decrypted_token = _jwt_decrypt(encrypted_token)

    if decrypted_token.get('roles'):
        current_user_permissions = map_role_to_permissions(decrypted_token["roles"])

        if 'flush' in current_user_permissions:
            user = _get_user(decrypted_token)
            _submit_data(user)
            get_questionnaire_store(user.user_id, user.user_ik).delete()
        else:
            raise FlushPermissionDenied("Your role doesn't have permission to flush data")
    else:
        raise FlushPermissionDenied("No role defined, you can't flush data")

    return Response(status=200)


def _submit_data(user):

    answer_store = get_answer_store(user)

    if answer_store.answers:
        metadata = get_metadata(user)
        json, schema = get_schema(metadata)
        routing_path = PathFinder(json, answer_store, metadata).get_routing_path()
        submitter = SubmitterFactory.get_submitter()
        message = convert_answers(metadata, schema, answer_store, routing_path)
        message['completed'] = False
        submitter.send_answers(message)
    else:
        raise NoSurveyDataToFlush("There are no answers to flush")


def _get_user(decrypted_token):
    user_id = UserIDGenerator.generate_id(decrypted_token)
    user_ik = UserIDGenerator.generate_ik(decrypted_token)
    return User(user_id, user_ik)


def _jwt_decrypt(encrypted_token):
    decoder = JWTDecryptor()
    decrypted_token = decoder.decrypt_jwt_token(encrypted_token)
    return decrypted_token
