from flask import render_template, json
from flask.ext.login import login_required
from .. import main_blueprint

from app.submitter.submitter import Submitter
from app import settings
from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

import logging


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/questionnaire/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('../data/mci.json') as f:
        data = json.load(f)
    return render_template('questionnaire.html', questionnaire=data)


@main_blueprint.route('/cover-page', methods=['GET'])
def cover_page():
    return render_template('cover-page.html')



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
