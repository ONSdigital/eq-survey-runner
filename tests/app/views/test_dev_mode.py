from tests.integration.integration_test_case import IntegrationTestCase


class TestDevMode(IntegrationTestCase):

    def test_dev_mode(self):
        response = self.client.get('/dev')
        self.assertEqual(response.status_code, 200)

    def test_dev_flush_mode(self):
        response = self.client.get('/dev/flush')
        self.assertEqual(response.status_code, 200)


    def test_dev_mode_submission(self):
        # Use the parameters from the dev page
        response = self.client.post('/dev', data=dict(
            exp="1800",
            schema="0_star_wars.json",
            period_str="May 2016",
            period_id="201605",
            collection_exercise_sid="789",
            ru_ref="12346789012A",
            ru_name="Apple",
            trad_as="Apple",
            ref_p_start_date="2016-05-01",
            ref_p_end_date="2016-05-31",
            return_by="2016-06-12",
            employment_date="2016-06-10",
            region_code="GB-GBN",
            user_id="test"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dev_flush_mode_submission(self):
        response = self.client.post('/dev/flush', data=dict(
            schema="1_0205.json",
            collection_exercise_sid="789",
            ru_ref="12346789012A",
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 404)
