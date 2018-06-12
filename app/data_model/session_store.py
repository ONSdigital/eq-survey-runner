from structlog import get_logger
import simplejson as json

from app.data_model.models import EQSession, db
from app.data_model.session_data import SessionData
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

    def create(self, eq_session_id, user_id, session_data):
        """
        Create a new eq_session and associate it with the user_id specified
        """
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self._eq_session = EQSession(self.eq_session_id, self.user_id)

        return self

    def save(self):
        """
        save session
        """
        if self._eq_session:
            self._eq_session.session_data = \
                StorageEncryption(self.user_id, self.user_ik, self.pepper).encrypt_data(vars(self.session_data))

            # pylint: disable=maybe-no-member
            db.session.add(self._eq_session)
            db.session.commit()

    def delete(self):
        """
        deletes user session from database
        """
        if self._eq_session:
            # pylint: disable=maybe-no-member
            db.session.delete(self._eq_session)
            db.session.commit()

            self._eq_session = None
            self.eq_session_id = None
            self.user_id = None
            self.session_data = None

    def _load(self):

        if self._eq_session:
            return self._eq_session

        if self.eq_session_id is None:
            return None

        logger.debug('finding eq_session_id in database', eq_session_id=self.eq_session_id)

        # pylint: disable=maybe-no-member
        # SQLAlchemy doing declarative magic which makes session scope query property available
        self._eq_session = EQSession.query.filter(EQSession.eq_session_id == self.eq_session_id).first()

        if self._eq_session:
            self.user_id = self._eq_session.user_id

            if self._eq_session.session_data:
                encrypted_session_data = self._eq_session.session_data
                session_data = StorageEncryption(self.user_id, self.user_ik, self.pepper)\
                    .decrypt_data(encrypted_session_data)

                self.session_data = json.loads(session_data, object_hook=lambda d: SessionData(**d))

            logger.debug('found matching eq_session for eq_session_id in database',
                         session_id=self._eq_session.eq_session_id,
                         user_id=self._eq_session.user_id)
        else:
            logger.debug('eq_session_id not found in database', eq_session_id=self.eq_session_id)

        return self._eq_session
