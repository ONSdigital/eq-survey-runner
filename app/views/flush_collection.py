import os
import boto3

from flask import Blueprint, session, request, current_app
from structlog import get_logger

from boto3.dynamodb.conditions import Key

from sdc.crypto.decrypter import decrypt
from app.keys import KEY_PURPOSE_AUTHENTICATION

from app.authentication.user import User

flush_collection_blueprint = Blueprint('flush_collection', __name__)


@flush_collection_blueprint.route('/flush_collection', methods=['POST'])
def flush_collection_data():

    logger = get_logger()

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if not encrypted_token or encrypted_token is None:
        return "Could not find expected request argument: token", 400

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    if not decrypted_token or decrypted_token is None:
        logger.info("Failed to decrypt given token")
        return 403

    collection_exercise_id = decrypted_token.get("collection_exercise_id")

    if not collection_exercise_id or collection_exercise_id is None:
        return "Could not find 'collection_exercise_id' in decrypted JWT", 400

    responses_to_flush = _get_partial_responses_for_collection(collection_exercise_id)

    for response in responses_to_flush:
        _flush_response(response)

    return "OK"


def _get_partial_responses_for_collection(collection_exercise_id, dynamodb=None):

    EQ_QUESTIONNAIRE_STATE_TABLE_NAME = os.environ.get("EQ_QUESTIONNAIRE_STATE_TABLE_NAME")

    if not EQ_QUESTIONNAIRE_STATE_TABLE_NAME or EQ_QUESTIONNAIRE_STATE_TABLE_NAME is None:
        return 500

    EQ_DYNAMODB_ENDPOINT = os.environ.get("EQ_DYNAMODB_ENDPOINT")

    if not EQ_DYNAMODB_ENDPOINT or EQ_DYNAMODB_ENDPOINT is None:
        return 500

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=EQ_DYNAMODB_ENDPOINT)

    table = dynamodb.Table(EQ_QUESTIONNAIRE_STATE_TABLE_NAME)

    scan_kwargs = {
        "FilterExpression": Key("collection_exercise_id").eq(collection_exercise_id)
    }

    response = table.scan(**scan_kwargs)

    return response.get('Items', [])


def _flush_response(response):

    user = _get_user(response)

    return "OK"


def _get_user(response):

    # TODO - Find a suitable way to get the RU REF, EQ_ID and Form Type. Maybe store unencrypted in DB but unsure on how safe this will be. Could decrypt the state data, 
    # but might be slow (?) and not sure how to do this on Runner.
    #  Seems to always need the user IK

    return "OK"
