import logging

from app.data_model.database import QuestionnaireState
from app.data_model.database import db_session

from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DatabaseStorage:
    '''
    Server side storage using an RDS database (where one column is the entire JSON representation of the questionnaire state)
    '''
    def store(self, data, user_id, user_ik=None):
        logger.debug("About to store data %s for user %s", data, user_id)
        if self.has_data(user_id):
            logger.debug("Loading previous data for user %s", user_id)
            questionnaire_state = self._get_object(user_id)
            logger.debug("Loaded %s", questionnaire_state)
            questionnaire_state.set_data(data)
        else:
            logger.debug("Creating questionnaire state for user %s with data %s", user_id, data)
            questionnaire_state = QuestionnaireState(user_id, data)

        logger.debug("Committing questionnaire state")

        try:
            db_session.add(questionnaire_state)
            db_session.commit()
            logger.debug("Committed")
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def get(self, user_id, user_ik=None):
        logger.debug("Loading questionnaire state for user %s", user_id)
        questionnaire_state = self._get_object(user_id)
        if questionnaire_state:
            data = questionnaire_state.get_data()
            logger.debug("Loaded data %s", data)
            return questionnaire_state.get_data()
        else:
            logger.debug("Return None from get")
            return None

    def _get_object(self, user_id):
        logger.debug("Get the questionnaire object for user %s", user_id)
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == user_id).first()

    def has_data(self, user_id):
        logger.debug("Running count query for user %s", user_id)
        count = QuestionnaireState.query.filter(QuestionnaireState.user_id == user_id).count()
        logger.debug("Number of entries for user %s is %s", user_id, count)
        return count > 0

    def delete(self, user_id):
        logger.debug("About to delete users %s data", user_id)
        if self.has_data(user_id):
            questionnaire_state = self._get_object(user_id)
            try:
                db_session.delete(questionnaire_state)
                db_session.commit()
                logger.debug("Deleted")
            except SQLAlchemyError:
                db_session.rollback()
                raise

    def clear(self):
        logger.warning("About to delete all questionnaire data")
        QuestionnaireState.query.delete()
        logger.warning("Deleted all questionnaire data")
