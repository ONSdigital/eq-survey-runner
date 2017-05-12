from structlog import get_logger
import json

from app.data_model.database import QuestionnaireState, dynamodb

table = dynamodb.Table('questionnaire_state')

logger = get_logger()


class QuestionnaireStorage:
    """
    Server side storage using an RDS database (where one column is the entire JSON representation of the questionnaire state)
    """

    def __init__(self, user_id):
        if user_id is None:
            raise ValueError('User id must be set')
        self.user_id = user_id

    def add_or_update(self, data):
        questionnaire_state = self._get()
        if questionnaire_state:
            logger.debug("updating questionnaire data", user_id=self.user_id)
            questionnaire_state.set_data(data)
        else:
            logger.debug("creating questionnaire data", user_id=self.user_id)
            questionnaire_state = QuestionnaireState(self.user_id, data)

        table.put_item(
            Item=questionnaire_state.__dict__
        )
        print("PutItem succeeded")

    def get_user_data(self):
        questionnaire_state = self._get()
        if questionnaire_state:
            return questionnaire_state.get_data()
        return None

    def _get(self):
        logger.debug("getting questionnaire data", user_id=self.user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available

        response = table.get_item(
            Key={
                'user_id': self.user_id
            }
        )
        if 'Item' in response:
            return QuestionnaireState(response['Item']['user_id'], json.loads(response['Item']['state']))

        return None

    def delete(self):
        logger.debug("deleting users data", user_id=self.user_id)
        questionnaire_state = self._get()
        if questionnaire_state:
            table.delete_item(
                Key={
                    'user_id': questionnaire_state.user_id
                }
            )
