from flask import Blueprint, Response, request, session, current_app
from sdc.crypto.encrypter import encrypt
from sdc.crypto.decrypter import decrypt


from app.authentication.user import User
from app.globals import get_answer_store, get_questionnaire_store, get_completed_blocks
from app.questionnaire.path_finder import PathFinder
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.submitter.converter import convert_answers
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

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    roles = decrypted_token.get('roles')

    if roles and 'flusher' in roles:
        user = _get_user(decrypted_token)
        if _submit_data(user):
            return Response(status=200)
        return Response(status=404)
    return Response(status=403)


def _submit_data(user):

    answer_store = get_answer_store(user)

    if answer_store:
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        answer_store = questionnaire_store.answer_store
        metadata = questionnaire_store.metadata

        schema = load_schema_from_metadata(metadata)
        completed_blocks = get_completed_blocks(user)
        routing_path = PathFinder(schema, answer_store, metadata, completed_blocks).get_full_routing_path()

        message = convert_answers(schema, questionnaire_store, routing_path, flushed=True)
        encrypted_message = encrypt(message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION)

        sent = current_app.eq['submitter'].send_message(encrypted_message, case_id=metadata.get('case_id'), tx_id=metadata.get('tx_id'))

        if not sent:
            raise SubmissionFailedException()

        get_questionnaire_store(user.user_id, user.user_ik).delete()
        return True

    return False


def _get_user(decrypted_token):
    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(decrypted_token)
    user_ik = id_generator.generate_ik(decrypted_token)
    return User(user_id, user_ik)
