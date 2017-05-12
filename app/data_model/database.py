import datetime
import json
import boto3
from dateutil import parser

from structlog import get_logger

logger = get_logger()

class QuestionnaireState():

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.state = json.dumps(data)

    def set_data(self, data):
        logger.debug("setting data for questionnaire state")
        self.state = json.dumps(data)

    def get_data(self):
        data = json.loads(self.state)
        logger.debug("loading questionnaire state")
        return data

    def __repr__(self):
        return "<QuestionnaireState('%s','%s')>" % (self.user_id, self.state)


class EQSession():

    def __init__(self, eq_session_id, user_id, timestamp=None):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        if timestamp:
            self.timestamp = parser.parse(timestamp)
        else:
            self.timestamp = datetime.datetime.now().__str__()

    def __repr__(self):
        return "<EQSession('%s', '%s', '%s')>" % (self.eq_session_id, self.user_id, self.timestamp)

class UsedJtiClaim():

    def __init__(self, jti_claim):
        self.jti_claim = jti_claim
        self.used_at = datetime.datetime.now().__str__()

    def __repr__(self):
        return "<UsedJtiClaim('%s', '%s')>" % (self.jti_claim, self.used_at)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
