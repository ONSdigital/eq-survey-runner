from flask import render_template, request, json
from .. import main_blueprint
from app.main import errors
from app.authentication.jwt_decoder import Decoder
from app.authentication.invalid_token_exception import InvalidTokenException
from app.authentication.no_token_exception import NoTokenException
from app.submitter.submitter import Submitter
from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from app import settings

import logging


EQ_URL_QUERY_STRING_JWT_FIELD_NAME = 'token'

if (settings.EQ_RRM_PUBLIC_KEY is None or settings.EQ_SR_PRIVATE_KEY is None):
    raise OSError('KEYMAT not configured correctly.')
else:
    decoder = Decoder(settings.EQ_RRM_PUBLIC_KEY, settings.EQ_SR_PRIVATE_KEY, "digitaleq")


@main_blueprint.before_request
def jwt_before_request():
    if settings.EQ_PRODUCTION:
        logging.info("Production mode")
        return jwt_decrypt()
    else:
        logging.warning("Developer mode")
        return developer_mode()


def developer_mode():
    token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
    if token:
        if token.count(".") == 4:
            logging.debug("Decrypting JWT token " + token)
            return jwt_decrypt()
        else:
            tokens = token.split(".")
            if len(tokens) == 3 and tokens[2]:
                logging.debug("Decoding signed JWT token " + token)
                return jwt_decode_signed()
            else:
                logging.debug("Decoding JWT token " + token)
                return jwt_decode()


def jwt_decrypt():
    try:
        encrypted_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decrypt_jwt_token(encrypted_token)
        send_to_mq(token)
        return render_template('index.html', token_id=encrypted_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode_signed():
    try:
        signed_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decode_signed_jwt_token(signed_token)
        send_to_mq(token)
        return render_template('index.html', token_id=signed_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


def jwt_decode():
    try:
        unsigned_token = request.args.get(EQ_URL_QUERY_STRING_JWT_FIELD_NAME)
        token = decoder.decode_jwt_token(unsigned_token)
        send_to_mq(token)
        return render_template('index.html', token_id=unsigned_token, token=token)
    except NoTokenException as e:
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        return errors.forbidden(e)


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/questionnaire/<questionnaire_id>', methods=['GET', 'POST'])
def questionnaire(questionnaire_id):
    # TODO implement me!
    questionnaire_model = create_model()
    return render_template('questionnaire.html', questionnaire=questionnaire_model)


@main_blueprint.route('/questionnaire/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('../data/mci.json') as f:
        data = json.load(f)
    return render_template('questionnaire.html', questionnaire=data)


@main_blueprint.route('/cover-page', methods=['GET'])
def cover_page():
    return render_template('cover-page.html')


def create_model():
    '''
    Temporary method to hard code a questionnaire model to get hamish started
    '''
    questionnaire = Questionnaire()
    questionnaire.id = "22"
    questionnaire.survey_id = "23"
    questionnaire.title = "Monthly Business Survey - Retail Sales Index"
    questionnaire.description = "MCI Description"

    group = Group()
    group.id = "14ba4707-321d-441d-8d21-b8367366e766"
    group.title = ""
    questionnaire.groups = [group]

    block = Block()
    block.id = "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
    block.title = "Monthly Business Survey"
    group.blocks = [block]

    section = Section()
    section.id = "2cd99c83-186d-493a-a16d-17cb3c8bd302"
    section.title = ""
    block.sections = [section]

    question = Question()
    question.id = "4ba2ec8a-582f-4985-b4ed-20355deba55a"
    question.title = "On 12 January 2016 what was the number of employees for the business named above?"
    question.description = "An employee is anyone aged 16 years or over that your organisation directly " \
                           "pays from its payroll(s), in return for carrying out a full-time or part-time " \
                           "job or being on a training scheme."
    section.questions = [question]

    response = Response()
    response.name = "29586b4c-fb0c-4755-b67d-b3cd398cb30a"
    response.id = "29586b4c-fb0c-4755-b67d-b3cd398cb30a"
    response.label = "Male employees working more than 30 hours per week?"
    response.guidance = "How many men work for your company?"
    response.type = "Integer"
    question.responses = [response]

    return questionnaire


@main_blueprint.route('/jwt', methods=['GET'])
def jwt():
    return jwt_decode()


@main_blueprint.route('/jwt_signed', methods=['GET'])
def jwt_signed():
    return jwt_decode_signed()


@main_blueprint.route('/jwt_encrypted', methods=['GET'])
def jwt_encrypted_key_exchange():
    return jwt_decrypt()


def send_to_mq(token):
    submitter = Submitter()
    submitter.send(token)
