import logging

from app.data_model.database import QuestionnaireState, commit_or_rollback
from app.data_model.database import db_session

logger = logging.getLogger(__name__)


class QuestionnaireStorage:
    """
    Server side storage using an RDS database (where one column is the entire JSON representation of the questionnaire state)
    """

    def __init__(self, user_id):
        if user_id is None:
            raise ValueError('User id must be set')
        self.user_id = user_id

    def add_or_update(self, data):
        logger.debug("About to store data %s for user %s", data, self.user_id)
        if self.exists():
            logger.debug("Updating data for user %s", self.user_id)
            questionnaire_state = self._get()
            questionnaire_state.set_data(data)
        else:
            logger.debug("Creating questionnaire state for user %s with data %s", self.user_id, data)
            questionnaire_state = QuestionnaireState(self.user_id, data)

        with commit_or_rollback(db_session):
            # pylint: disable=maybe-no-member
            # session has a add function but it is wrapped in a session_scope which confuses pylint
            db_session.add(questionnaire_state)

    def get_user_data(self):
        return self._get().get_data()

    def _get(self):
        logger.debug("Get the questionnaire object for user %s", self.user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == self.user_id).first()

    def exists(self):
        logger.debug("Running count query for user %s", self.user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        count = QuestionnaireState.query.filter(QuestionnaireState.user_id == self.user_id).count()
        logger.debug("Number of entries for user %s is %s", self.user_id, count)
        return count > 0

    def delete(self):
        logger.debug("Deleting users %s data", self.user_id)
        if self.exists():
            questionnaire_state = self._get()
            with commit_or_rollback(db_session):
                # pylint: disable=maybe-no-member
                # session has a delete function but it is wrapped in a session_scope which confuses pylint
                db_session.delete(questionnaire_state)
