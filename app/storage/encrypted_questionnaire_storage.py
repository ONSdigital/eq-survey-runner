import hashlib

from structlog import get_logger

from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

from app.data_model.database import QuestionnaireState, commit_or_rollback
from app.data_model.database import db_session

logger = get_logger()


class EncryptedQuestionnaireStorage:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')
        if user_ik is None:
            raise ValueError('User ik must be set')
        if pepper is None:
            raise ValueError('Pepper must be set')
        self._encryption = JWEDirEncrypter()
        self._decryption = JWEDirDecrypter()
        self._user_id = user_id

        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode('utf-8'))
        sha256.update(to_str(user_ik).encode('utf-8'))
        sha256.update(to_str(pepper).encode('utf-8'))

        # we only need the first 32 characters for the CEK
        self._cek = to_bytes(sha256.hexdigest()[:32])

    def add_or_update(self, data):
        encrypted_data = self._encrypt_data(data)
        questionnaire_state = self._get()
        if questionnaire_state:
            logger.debug("updating questionnaire data", user_id=self._user_id)
            questionnaire_state.set_data(encrypted_data)
        else:
            logger.debug("creating questionnaire data", user_id=self._user_id)
            questionnaire_state = QuestionnaireState(self._user_id, encrypted_data)

        with commit_or_rollback(db_session):
            # pylint: disable=maybe-no-member
            # session has a add function but it is wrapped in a session_scope which confuses pylint
            db_session.add(questionnaire_state)

    def get_user_data(self):
        data = self._get_questionnaire_state()
        if data is not None and 'data' in data:
            decrypted_data = self._decrypt_data(data)
            return decrypted_data

    def delete(self):
        logger.debug("deleting users data", user_id=self._user_id)
        questionnaire_state = self._get()
        if questionnaire_state:
            with commit_or_rollback(db_session):
                # pylint: disable=maybe-no-member
                # session has a delete function but it is wrapped in a session_scope which confuses pylint
                db_session.delete(questionnaire_state)

    def _encrypt_data(self, data):
        encrypted = self._encryption.encrypt(data, self._cek)
        return {'data': encrypted}

    def _decrypt_data(self, encrypted_data):
        return self._decryption.decrypt(encrypted_data['data'], self._cek)

    def _get_questionnaire_state(self):
        questionnaire_state = self._get()
        if questionnaire_state:
            return questionnaire_state.get_data()
        return None

    def _get(self):
        logger.debug("getting questionnaire data", user_id=self._user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == self._user_id).first()
