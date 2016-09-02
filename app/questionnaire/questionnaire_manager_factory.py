import logging

from app import settings

from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.questionnaire.state_manager import StateManager
from app.questionnaire.state_recovery import StateRecovery
from app.utilities.schema import get_schema


logger = logging.getLogger(__name__)


class QuestionnaireManagerFactory(object):

    @staticmethod
    def get_instance():
        logger.debug("QuestionManagerFactory - get instance")
        if StateManager.has_state():
            logger.debug("StateManager loading state")
            state = StateManager.get_state()

            # TODO remove attribute check. This is for data migration in production and can be removed at a later date
            if hasattr(state, 'revision'):
                if state.revision == settings.EQ_GIT_REF:
                    questionnaire_manager = QuestionnaireManager(state.schema,
                                                                 current=state.current,
                                                                 first=state.first,
                                                                 tail=state.tail,
                                                                 archive=state.archive,
                                                                 valid_locations=state.valid_locations,
                                                                 submitted_at=state.submitted_at)
                else:
                    questionnaire_manager = QuestionnaireManager(QuestionnaireManagerFactory._get_schema())
                    StateRecovery.recover_from_post_data(questionnaire_manager)
            else:
                logger.error("Data not recoverable, old version of state without revision attribute")
                questionnaire_manager = QuestionnaireManager(QuestionnaireManagerFactory._get_schema())
        else:
            logger.debug("QuestionnaireManagerFactory - constructing new instance")
            questionnaire_manager = QuestionnaireManager(QuestionnaireManagerFactory._get_schema())
            questionnaire_manager.go_to(questionnaire_manager.get_first_location())

        # immediately save it to the database
        StateManager.save_state(questionnaire_manager.construct_state())
        logger.debug("QuestionnaireManagerFactory savingstate")
        return questionnaire_manager

    @staticmethod
    def _get_schema():
        # exists to facilitate testing
        return get_schema()
