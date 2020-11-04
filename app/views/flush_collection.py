from flask import Blueprint, session, request, current_app

from sdc.crypto.decrypter import decrypt
from app.keys import KEY_PURPOSE_AUTHENTICATION

flush_collection_blueprint = Blueprint('flush_collection', __name__)


@flush_collection_blueprint.route('/flush_collection', methods=['POST'])
def flush_collection_data():

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if not encrypted_token or encrypted_token is None:
        return 400

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    if not decrypted_token or decrypted_token is None:
        return 403

    collection_exercise_id = decrypted_token.get("collection_exercise_id")

    if not collection_exercise_id or collection_exercise_id is None:
        return 400

    print(collection_exercise_id)

    return "OK"
