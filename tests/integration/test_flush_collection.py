from mock import patch
from tests.integration.integration_test_case import IntegrationTestCase


class TestFlushCollection(IntegrationTestCase):

    def setUp(self):
        self.submitter_patcher = patch('app.setup.LogSubmitter')
        mock_submitter_class = self.submitter_patcher.start()
        self.submitter_instance = mock_submitter_class.return_value
        self.submitter_instance.send_message.return_value = True

        self.encrypter_patcher = patch('app.views.flush.encrypt')
        mock_encrypter_class = self.encrypter_patcher.start()
        self.encrypt_instance = mock_encrypter_class

        super().setUp()
        self.launchSurvey('test', '0205')
        self.post(action='start_questionnaire')

        form_data = {
            'period-from-day': '01',
            'period-from-month': '4',
            'period-from-year': '2016',
            'period-to-day': '30',
            'period-to-month': '4',
            'period-to-year': '2016',
            'total-retail-turnover': '100000'
        }
        self.post(form_data)

    def tearDown(self):
        self.submitter_patcher.stop()
        self.encrypter_patcher.stop()

        super().tearDown()

    def test_no_token(self):
        """GIVEN the endpoint is called,
        WHEN the application tries to find
        the expected token in the request
        query parameters
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        """

        self.post(url='/flush_collection')

        self.assertStatusCode(400)

    def test_cannot_decrypt_token(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        WHEN the application tries to decrypt it
        AND fails
        THEN the request should respond with:

        HTTP/1.1 403 Forbidden
        """

        self.post(url='/flush_collection?token=someInvalidJWT123')

        self.assertStatusCode(403)

    def test_cannot_find_collection_id(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        WHEN the application tries to find 
        the 'collection_exercise_id' property
        AND it is not there
        THEN the request should respond with:

        HTTP/1.1 400 Bad Request
        """

        token = 'eyJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAiLCJraWQiOiJlMTkwOTEwNzJmOTIwY2JmM2NhOWY0MzZjZWJhMzA5ZTdkODE0YTYyIn0.GRJW2ZweO49P9QY2CvH1Gbt4oBN32sXh02u-y73fy_TAXt01yrschnonSkw4cJJBop4pHPI8bzZiDGf-hnYKO2ZFfjN8KEEJ4XEvuMyBxHTmkNVxD8koP-krEF8GuOli0UgKOIrILf_ryJQKe4ly_zVg2ukyyjmr0usixlKWMW28QCa6UII1wzcPjvgM63YHT9AkpdZjZ_otIJCPhUkcdsj8eICV8ceoXQCJFWOH13ACGSmmg-_HZ5p6mW53NlPwBnEH7AGHAcYZMn6JPnZDCtQNz7dPdcsZKEnLUGw3AUBDHiCjMjtYjzycHMvemtwMwgUdxqOX019Vw7J2MsNRYw.J54iL6bCyecbOqVi.SrvqGCAVghvXKTAxeJXtJdHYTswogyrKMdhPWEpU2ILnebrVpzjoYndZRI45Plb3pNLm9oXnhCzMBAyUq3W3WYKREaUa9LPfZen5NtJKiAThWTl86VG6m_oFIZjEtPqFYyIWBeuL5eApAGVKCv0qVpUbh9OYOlFLjorudoo3myuLHbOYjQ9uhK04xfBrjbT_oIlL37ZhLKMvANJJCXa-nIaSujAitBcb_NVMk6O-2XrCsbnQhI78UWtPRBGlcc4Lwbol4w3qsffEt0qJJZ5ZRshG3Ifo8f6N2FCvOEvXzUZbLhvk5d4-v2_W0jjsQp6vMeVXpoqzBqQJ4D1xkcA7lVA-XNls6dmh_GeoINig-ZWWvxVnZEn5GYpjFXG03s54ewkUeUDctETiIq2wWcEeM_LsICHV2a5OSzc2gfLddXGsRWMZ7CAAxhUchU9JcX9_cZBI9eJ89UiiaYG1S-3mXF4AYmdiZG4kki-u1RwjJEyKnsdFHXUOJ8AE_dgpKRu3mf3UCqhORetcrxT-PoZNBIB2O3DFzijZ-iztiYppkKlFVzBxdXw6LytcWkmV9rhiuZOnGdAZq4nNyMz4sNKPUSJ1mulB-FQiByuNavWwEbfCng.1AyTaHMxp9S_HQscyohE2Q'
        url = '/flush_collection?token=' + token

        self.post(url=url)

        self.assertStatusCode(400)

    def test_successful_flush_no_fails(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        AND the application can find the 
        'collection_exercise_id' property,
        AND there are partial responses for
        the given collection exercise
        AND the application is able to flush them 
        THEN the request should respond with:

        HTTP/1.1 200 OK
        ((JSON string as documented))
        """

        # TODO

    def test_failed_flush(self):
        """GIVEN the endpoint is called,
        AND a token is given,
        AND the token can be decrypted,
        AND the application can find the 
        'collection_exercise_id' property,
        AND there are partial responses for
        the given collection exercise
        AND the application is not able to flush them 
        THEN the request should respond with:

        HTTP/1.1 200 OK
        ((JSON string as documented))
        """

        # TODO
