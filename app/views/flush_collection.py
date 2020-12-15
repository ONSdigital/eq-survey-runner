import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from structlog import get_logger
from flask import Blueprint, request, session, current_app, g
from sdc.crypto.encrypter import encrypt
from sdc.crypto.decrypter import decrypt
from app.authentication.user import User
from app.globals import (get_answer_store, get_metadata, get_questionnaire_store,
                         get_completed_blocks, get_collection_metadata)
from app.questionnaire.path_finder import PathFinder
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.schema import load_schema_from_metadata

logger = get_logger()

flush_collection_blueprint = Blueprint('flush_collection', __name__)


@flush_collection_blueprint.route('/flush_collection', methods=['POST'])
def flush_collection_data():
    """Resolver function for the /flush_collection endpoint. Retrieves partial responses
    for a given collection_id and attempts to push them into EQs Rabbit queue.

    Parameters:
         A JSON object of the following schema, encoded in a JWT token:
        {
             'collection_exercise_id': STRING
        }

    Returns:
        A JSON object of the following schema:
        {
            'collection_exercise_id': STRING
            'total_partial_responses': INT
            'successful_flush: [
                {
                    'user_id': STRING
                    'ru_ref': STRING
                    'eq_id': STRING
                    'form_type': STRING
                }
            ]
            'failed_flush: [
                {
                    'user_id': STRING
                    'ru_ref': STRING
                    'eq_id': STRING
                    'form_type': STRING
                }
            ]
        }
    """

    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if not encrypted_token or encrypted_token is None:
        return 'Could not find expected request argument: token', 400

    decrypted_token = decrypt(token=encrypted_token,
                              key_store=current_app.eq['key_store'],
                              key_purpose=KEY_PURPOSE_AUTHENTICATION,
                              leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'])

    if not decrypted_token or decrypted_token is None:
        logger.info('Failed to decrypt given token')
        return 403

    collection_exercise_id = decrypted_token.get('collection_exercise_id')

    if not collection_exercise_id or collection_exercise_id is None:
        return 'Could not find "collection_exercise_id" in decrypted JWT', 400

    responses_to_flush = _get_partial_responses_for_collection(collection_exercise_id)

    api_response = {
        'collection_exercise_id': collection_exercise_id,
        'total_partial_responses': len(responses_to_flush),
        'successful_flush': [],
        'failed_flush': [],
    }

    for response in responses_to_flush:
        status, response_summary = _flush_response(response)
        if status:
            api_response['successful_flush'].append(response_summary)
        else:
            api_response['failed_flush'].append(response_summary)

    return json.dumps(api_response)


def _get_partial_responses_for_collection(collection_exercise_id, dynamodb=None):
    """Accesses the Questionnaire State DynamoDB table and retrieves all records featuring
    a given collection_exercise_id.

    Parameters:
        collection_exercise_id (STRING): The ID of the collection exercise to flush.
        dynamodb (CLASS): An instance of DynamoDB for accessing the database.

    Returns:
        A list of objects, each being an individual partial response.
    """

    EQ_QUESTIONNAIRE_STATE_TABLE_NAME = os.environ.get('EQ_QUESTIONNAIRE_STATE_TABLE_NAME')

    if not EQ_QUESTIONNAIRE_STATE_TABLE_NAME or EQ_QUESTIONNAIRE_STATE_TABLE_NAME is None:
        return 500

    if not dynamodb:
        EQ_DYNAMODB_ENDPOINT = os.environ.get('EQ_DYNAMODB_ENDPOINT')
        if not EQ_DYNAMODB_ENDPOINT or EQ_DYNAMODB_ENDPOINT is None:
            return 500

        dynamodb = boto3.resource('dynamodb', endpoint_url=EQ_DYNAMODB_ENDPOINT)

    table = dynamodb.Table(EQ_QUESTIONNAIRE_STATE_TABLE_NAME)

    scan_kwargs = {
        'FilterExpression': Key('collection_exercise_id').eq(collection_exercise_id),
    }

    response = table.scan(**scan_kwargs)

    return response.get('Items', [])


def _flush_response(response):
    """Given a single response, tries to find the user who created it and calls a method to attempt
    the flushing.

    Parameters:
        response (Dict): An individual partial response from the database

    Returns:
        Boolean: Whether or not the response was successfully flushed
        response_summary (Dict): Abstract information about the response that we tried to flush
    """

    response_summary = {
        'collection_exercise_sid': response.get('collection_exercise_id'),
        'user_id': response.get('user_id'),
        'ru_ref': response.get('ru_ref'),
        'eq_id': response.get('eq_id'),
        'form_type': response.get('form_type'),
    }

    user = _get_user(response_summary)

    response_summary.pop('collection_exercise_sid')

    if _submit_data(user):
        return True, response_summary

    return False, response_summary


def _get_user(response):
    """Generates user locators from their response and retrieves their information.

    Parameters:
        response (Dict): An individual partial response from the database.

    Returns:
        User (Class): An individual user
    """

    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(response)
    user_ik = id_generator.generate_ik(response)
    return User(user_id, user_ik)


def _submit_data(user):
    """Encrypts and pushes a users partial response to EQs Rabbit queue.

    Paramaters:
        User (Class): Information about a particular user, including their partial responses.

    Returns:
        Boolean: Whether or not the submission was successful.
    """

    g.pop('_questionnaire_store', None)
    answer_store = get_answer_store(user)

    if answer_store:
        metadata = get_metadata(user)
        collection_metadata = get_collection_metadata(user)
        schema = load_schema_from_metadata(metadata)
        completed_blocks = get_completed_blocks(user)
        routing_path = PathFinder(schema, answer_store, metadata, completed_blocks).get_full_routing_path()

        message = convert_answers(metadata, collection_metadata, schema, answer_store, routing_path, flushed=True)
        encrypted_message = encrypt(message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION)

        sent = current_app.eq['submitter'].send_message(encrypted_message, current_app.config['EQ_RABBITMQ_QUEUE_NAME'], metadata['tx_id'])

        if not sent:
            raise SubmissionFailedException()

        get_questionnaire_store(user.user_id, user.user_ik).delete()

        return True

    return False
