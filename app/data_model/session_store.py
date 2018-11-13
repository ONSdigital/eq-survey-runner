import simplejson as json
from jwcrypto.common import base64url_decode
from structlog import get_logger

from app.data_model.app_models import EQSession
from app.data_model.session_data import SessionData
from app.storage import data_access
from app.storage.storage_encryption import StorageEncryption

logger = get_logger()


class SessionStore:

    def __init__(self, user_ik, pepper, eq_session_id=None):
        self.eq_session_id = eq_session_id
        self.user_id = None
        self.user_ik = user_ik
        self.session_data = None
        self._eq_session = None
        self.pepper = pepper
        if eq_session_id:
            self._load()

    @property
    def expiration_time(self):
        """
        Checking if expires_at is available can be removed soon after deployment,
        it is only needed to cater for in-flight sessions.
        """
        if self._eq_session and self._eq_session.expires_at:
            return self._eq_session.expires_at

    @expiration_time.setter
    def expiration_time(self, expires_at):
        """
        Checking if expires_at is available can be removed soon after deployment,
        it is only needed to cater for in-flight sessions.
        """
        if self._eq_session and self._eq_session.expires_at:
            self._eq_session.expires_at = expires_at

    def create(self, eq_session_id, user_id, session_data, expires_at=None):
        """
        Create a new eq_session and associate it with the user_id specified
        """
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self._eq_session = EQSession(self.eq_session_id, self.user_id, expires_at=expires_at)

        return self

    def save(self):
        """
        save session
        """
        if self._eq_session:
            self._eq_session.session_data = \
                StorageEncryption(self.user_id, self.user_ik, self.pepper).encrypt_data(vars(self.session_data))

            data_access.put(self._eq_session)

        return self

    def delete(self):
        """
        deletes user session from database
        """
        if self._eq_session:
            data_access.delete(self._eq_session)

            self._eq_session = None
            self.eq_session_id = None
            self.user_id = None
            self.session_data = None

    def _load(self):
        logger.debug('finding eq_session_id in database', eq_session_id=self.eq_session_id)

        self._eq_session = data_access.get_by_key(EQSession, self.eq_session_id)

        if self._eq_session:

            self.user_id = self._eq_session.user_id

            if self._eq_session.session_data:
                encrypted_session_data = self._eq_session.session_data
                session_data = StorageEncryption(self.user_id, self.user_ik, self.pepper) \
                    .decrypt_data(encrypted_session_data)

                session_data = session_data.decode()
                # for backwards compatibility
                # session data used to be base64 encoded before encryption
                try:
                    session_data = base64url_decode(session_data).decode()
                except ValueError:
                    pass

                self.session_data = json.loads(session_data, object_hook=lambda d: SessionData(**d))

            logger.debug('found matching eq_session for eq_session_id in database',
                         session_id=self._eq_session.eq_session_id,
                         user_id=self._eq_session.user_id)
        else:
            logger.debug('eq_session_id not found in database', eq_session_id=self.eq_session_id)

        return self._eq_session
