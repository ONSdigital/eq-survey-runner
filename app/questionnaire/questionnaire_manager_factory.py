import logging

from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.questionnaire.user_journey_manager import UserJourneyManager

from app.utilities.schema import get_schema


logger = logging.getLogger(__name__)


class QuestionnaireManagerFactory(object):

    @staticmethod
    def get_instance():
        logger.debug("QuestionManagerFactory - get instance")
        if UserJourneyManager.has_user_journey():
            logger.debug("StateManager loading state")
            state = UserJourneyManager.get_user_journey()

            questionnaire_manager = QuestionnaireManager(QuestionnaireManagerFactory._get_schema(),
                                                         current=state.current,
                                                         first=state.first,
                                                         tail=state.tail,
                                                         archive=state.archive,
                                                         valid_locations=state.valid_locations,
                                                         submitted_at=state.submitted_at)
        else:
            logger.debug("QuestionnaireManagerFactory - constructing new instance")
            questionnaire_manager = QuestionnaireManager(QuestionnaireManagerFactory._get_schema())
            questionnaire_manager.go_to(questionnaire_manager.get_first_location())

        # immediately save it to the database
        logger.debug("QuestionnaireManagerFactory saving state")
        return questionnaire_manager

    @staticmethod
    def _get_schema():
        # exists to facilitate testing
        return get_schema()
