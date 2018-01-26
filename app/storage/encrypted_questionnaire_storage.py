import simplejson as json

from structlog import get_logger

from app.storage.storage_encryption import StorageEncryption
from app.data_model.models import QuestionnaireState, db
logger = get_logger()


class EncryptedQuestionnaireStorage:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')

        self._user_id = user_id
        self.encrypter = StorageEncryption(user_id, user_ik, pepper)

    def add_or_update(self, data, version):
        encrypted_data = self.encrypter.encrypt_data(data)
        encrypted_data_json = json.dumps({'data': encrypted_data})
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            logger.debug('updating questionnaire data', user_id=self._user_id)
            questionnaire_state.state = encrypted_data_json
            questionnaire_state.version = version
        else:
            logger.debug('creating questionnaire data', user_id=self._user_id)
            questionnaire_state = QuestionnaireState(self._user_id, encrypted_data_json, version)

        # session has a add function but it is wrapped in a session_scope which confuses pylint
        # pylint: disable=maybe-no-member
        db.session.add(questionnaire_state)
        db.session.commit()

    def get_user_data(self):
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            data = json.loads(questionnaire_state.state)
            version = questionnaire_state.version or 0

            if 'data' in data:
                decrypted_data = self.encrypter.decrypt_data(data['data'])
                return decrypted_data, version

        return None, None

    def delete(self):
        logger.debug('deleting users data', user_id=self._user_id)
        questionnaire_state = self._find_questionnaire_state()
        if questionnaire_state:
            # session has a delete function but it is wrapped in a session_scope which confuses pylint
            # pylint: disable=maybe-no-member
            db.session.delete(questionnaire_state)
            db.session.commit()

    def _find_questionnaire_state(self):
        logger.debug('getting questionnaire data', user_id=self._user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == self._user_id).first()
