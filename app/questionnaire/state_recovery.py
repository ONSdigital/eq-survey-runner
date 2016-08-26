import logging


from flask_login import current_user


from werkzeug.datastructures import ImmutableMultiDict, MultiDict

logger = logging.getLogger(__name__)

POST_DATA = "post_data"


class StateRecovery(object):

    @staticmethod
    def save_post_date(location, post_data):
        logger.debug("Saving Post Data %s", post_data)
        questionnaire_data = current_user.get_questionnaire_data()
        if POST_DATA not in questionnaire_data:
            questionnaire_data[POST_DATA] = []

        questionnaire_data[POST_DATA].append({'location': location, 'post_data': StateRecovery._convert_to_dict(post_data)})
        current_user.save()

    @staticmethod
    def _convert_to_dict(post_data):
        logger.error("Multi dict is %s", post_data)
        return post_data.to_dict(flat=False)

    @staticmethod
    def recover_from_post_data(questionnaire_manager):
        logger.debug("Recovering from post data")

        logger.debug("Retrieving questionnaire data")
        questionnaire_data = current_user.get_questionnaire_data()
        if POST_DATA not in questionnaire_data:
            questionnaire_data[POST_DATA] = []

        all_post_data = questionnaire_data[POST_DATA]
        logger.debug("All post data %s", all_post_data)
        questionnaire_manager.go_to(questionnaire_manager.get_first_location())

        # basically this replays the post data in order
        for post_data in all_post_data:
            logger.debug("Replaying post data %s", post_data)
            location = post_data['location']
            data_to_replay = StateRecovery._convert_to_multi_dict(post_data['post_data'])
            location = questionnaire_manager.process_incoming_answers(location, data_to_replay, replay=True)
            questionnaire_manager.go_to(location)
            logger.debug("Location %s", location)
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
