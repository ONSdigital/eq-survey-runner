from uuid import UUID

from sqlalchemy.exc import IntegrityError
from structlog import get_logger

from app.data_model.database import UsedJtiClaim, commit_or_rollback, db_session

logger = get_logger()


class JtiTokenUsed(Exception):

    def __init__(self, jti_claim):
        super().__init__()
        self.jti_claim = jti_claim

    def __str__(self, *args, **kwargs):
        return "jti claim '{jti_claim}' has already been used".format(jti_claim=self.jti_claim)


def _is_valid(jti_claim):
    try:
        UUID(jti_claim, version=4)
    except ValueError:
        return False
    return True


def use_jti_claim(jti_claim):
    """
    Use a jti claim
    :param jti_claim: jti claim to mark as used.
    :raises ValueError: when jti_claim is None.
    :raises TypeError: when jti_claim is not a valid uuid4.
    :raises JtiTokenUsed: when jti_claim has already been used.
    """
    if jti_claim is None:
        raise ValueError
    if not _is_valid(jti_claim):
        logger.info("jti claim is invalid", jti_claim=jti_claim)
        raise TypeError

    try:
        with commit_or_rollback(db_session):
            jti = UsedJtiClaim(jti_claim)
            # pylint: disable=maybe-no-member
            # db_session has an add function but it is wrapped in a session_scope which confuses pylint
            db_session.add(jti)
    except IntegrityError as e:
        logger.error("jti claim has already been used", jti_claim=jti_claim)
        raise JtiTokenUsed(jti_claim) from e
