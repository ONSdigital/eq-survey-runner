from uuid import UUID

from datetime import datetime, timedelta
from dateutil.tz import tzutc
from structlog import get_logger

from app.data_model.app_models import UsedJtiClaim
from app.storage import data_access
from app.storage.errors import ItemAlreadyExistsError

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


def use_jti_claim(jti_claim, expires):
    """
    Use a jti claim
    :param jti_claim: jti claim to mark as used.
    :param expires: when the jti claim expires.
    :raises ValueError: when jti_claim is None.
    :raises TypeError: when jti_claim is not a valid uuid4.
    :raises JtiTokenUsed: when jti_claim has already been used.
    """
    if jti_claim is None:
        raise ValueError
    if not _is_valid(jti_claim):
        logger.info('jti claim is invalid', jti_claim=jti_claim)
        raise TypeError

    try:
        used_at = datetime.now(tz=tzutc())
        # Make claim expire a little later than exp to avoid race conditions with out of sync clocks.
        expires += timedelta(seconds=60)

        jti = UsedJtiClaim(jti_claim, used_at, expires)

        data_access.put(jti, overwrite=False)
    except ItemAlreadyExistsError as e:
        logger.error('jti claim has already been used', jti_claim=jti_claim)
        raise JtiTokenUsed(jti_claim) from e
