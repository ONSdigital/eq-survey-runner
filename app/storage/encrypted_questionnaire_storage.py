import hashlib
import simplejson as json

from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode, base64url_decode
from structlog import get_logger

from app.data_model.models import QuestionnaireState, db
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class EncryptedQuestionnaireStorage:

    def __init__(self, user_id, user_ik, pepper):
        if user_id is None:
            raise ValueError('User id must be set')
        if user_ik is None:
            raise ValueError('User ik must be set')
        if pepper is None:
            raise ValueError('Pepper must be set')
        self._user_id = user_id
        self._cek = self._generate_key(user_id, user_ik, pepper)

    def add_or_update(self, data, version):
        encrypted_data = self._encrypt_data(data)
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
                decrypted_data = self._decrypt_data(data['data'])
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

    @staticmethod
    def _generate_key(user_id, user_ik, pepper):
        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode('utf-8'))
        sha256.update(to_str(user_ik).encode('utf-8'))
        sha256.update(to_str(pepper).encode('utf-8'))

        # we only need the first 32 characters for the CEK
        return to_bytes(sha256.hexdigest()[:32])

    def _encrypt_data(self, data):
        protected_header = {
            'alg': 'dir',
            'enc': 'A256GCM',
            'kid': '1,1',
        }
        jwe_token = jwe.JWE(plaintext=base64url_encode(data), protected=protected_header)

        key = self.generate_jwk_from_cek(self._cek)

        jwe_token.add_recipient(key)

        return jwe_token.serialize(compact=True)

    def _decrypt_data(self, encrypted_token):

        key = self.generate_jwk_from_cek(self._cek)

        jwe_token = jwe.JWE(algs=['dir', 'A256GCM'])
        jwe_token.deserialize(encrypted_token, key)

        return base64url_decode(jwe_token.payload.decode()).decode()

    def _find_questionnaire_state(self):
        logger.debug('getting questionnaire data', user_id=self._user_id)
        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        return QuestionnaireState.query.filter(QuestionnaireState.user_id == self._user_id).first()

    @staticmethod
    def generate_jwk_from_cek(cek):
        password = {
            'kty': 'oct',
            'k': base64url_encode(cek),
        }

        return jwk.JWK(**password)
