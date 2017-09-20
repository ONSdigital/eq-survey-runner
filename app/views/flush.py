from flask import Blueprint, Response, request, session, current_app
from sdc.crypto.decrypter import decrypt

from app.authentication.authenticator import decrypt_jwe, decode_jwt
from app.authentication.user import User
from app.globals import get_answer_store, get_metadata, get_questionnaire_store
from app.questionnaire.path_finder import PathFinder
from app.secrets import KEY_PURPOSE_AUTHENTICATION
from app.submitter.converter import convert_answers
from app.submitter.encrypter import encrypt
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.schema import load_schema_from_metadata

flush_blueprint = Blueprint('flush', __name__)


@flush_blueprint.route('/flush', methods=['POST'])
def flush_data():

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if not encrypted_token or encrypted_token is None:
        return Response(status=403)

    decrypted_token = decrypt(encrypted_token, current_app.eq['secret_store'], purpose=KEY_PURPOSE_AUTHENTICATION)

    # jwt_token = decrypt_jwe(encrypted_token, current_app.eq['secret_store'], purpose=KEY_PURPOSE_AUTHENTICATION)
    #
    # decrypted_token = decode_jwt(jwt_token, current_app.eq['secret_store'], purpose=KEY_PURPOSE_AUTHENTICATION)

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

        message = convert_answers(metadata, schema, answer_store, routing_path, flushed=True)
        encrypted_message = encrypt(message, current_app.eq['secret_store'])

        sent = current_app.eq['submitter'].send_message(encrypted_message, current_app.config['EQ_RABBITMQ_QUEUE_NAME'], metadata["tx_id"])

        if not sent:
            raise SubmissionFailedException()

        get_questionnaire_store(user.user_id, user.user_ik).delete()
        return True
    else:
        return False


def _get_user(decrypted_token):
    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(decrypted_token)
    user_ik = id_generator.generate_ik(decrypted_token)
    return User(user_id, user_ik)
