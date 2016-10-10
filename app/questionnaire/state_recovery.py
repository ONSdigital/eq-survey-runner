import logging

from app import settings
from app.data_model.questionnaire_store import get_questionnaire_store

from flask_login import current_user

from werkzeug.datastructures import ImmutableMultiDict, MultiDict

logger = logging.getLogger(__name__)

POST_DATA = "post_data"
MAX_NO_OF_REPLAYS = settings.EQ_MAX_REPLAY_COUNT


class StateRecovery(object):

    @staticmethod
    def save_post_date(location, post_data):
        logger.debug("Saving Post Data %s", post_data)
        store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        if POST_DATA not in store.data:
            store.data[POST_DATA] = []

        store.data[POST_DATA].append({'location': location, 'post_data': post_data.to_dict(flat=False)})
        store.save()

    @staticmethod
    def recover_from_post_data(questionnaire_manager):
        logger.debug("Recovering from post data")

        logger.debug("Retrieving questionnaire data")
        store = get_questionnaire_store(current_user.user_id, current_user.user_ik)
        if POST_DATA not in store.data:
            store.data[POST_DATA] = []

        all_post_data = store.data[POST_DATA]
        logger.debug("All post data %s", all_post_data)
        questionnaire_manager.go_to(questionnaire_manager.get_first_location())

        # basically this replays the post data in order
        replay_counter = 0
        for post_data in all_post_data:
            logger.debug("MAX_NO_OF_REPLAYS %s", MAX_NO_OF_REPLAYS)
            if replay_counter < MAX_NO_OF_REPLAYS:
                logger.debug("Replay count %s", replay_counter)
                logger.debug("Replaying post data %s", post_data)
                location = post_data['location']
                data_to_replay = StateRecovery._convert_to_multi_dict(post_data['post_data'])
                location = questionnaire_manager.process_incoming_answers(location, data_to_replay, replay=True)
                questionnaire_manager.go_to(location)
                logger.debug("Location %s", location)
                replay_counter += 1
            else:
                logger.error("Exceeded maximum number of replays")
        logger.debug("Post data replayed")

        return questionnaire_manager

    @staticmethod
    def _convert_to_multi_dict(post_data):
        multi_dict = MultiDict()
        for key in post_data.keys():
            for value in post_data[key]:
                multi_dict.add(key, value)

        logger.debug("Recovered multi dict is %s", multi_dict)
        return ImmutableMultiDict(multi_dict)
