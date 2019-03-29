from datetime import datetime, timedelta
import uuid

import fakeredis

from app.storage.errors import ItemAlreadyExistsError
from app.storage.redis import RedisStorage
from app.data_model.app_models import UsedJtiClaim
from tests.app.app_context_test_case import AppContextTestCase


class TestDatastore(AppContextTestCase):

    def setUp(self):
        super().setUp()

        self.mock_client = fakeredis.FakeStrictRedis()

        self.redis = RedisStorage(self.mock_client)

    def test_put_jti(self):
        used_at = datetime.now()
        expires = used_at + timedelta(seconds=60)

        jti = UsedJtiClaim(str(uuid.uuid4()), used_at, expires)

        self.redis.put_jti(jti)

        set_data = self.mock_client.get(jti.jti_claim)

        self.assertEqual(int(jti.used_at.timestamp()), int(set_data))

    def test_duplicate_put_jti_fails(self):
        used_at = datetime.now()
        expires = used_at + timedelta(seconds=60)

        jti = UsedJtiClaim(str(uuid.uuid4()), used_at, expires)

        self.redis.put_jti(jti)

        with self.assertRaises(ItemAlreadyExistsError):
            self.redis.put_jti(jti)
