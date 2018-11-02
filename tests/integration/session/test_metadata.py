from tests.integration.integration_test_case import IntegrationTestCase

def get_metadata_for_metadata_survey():
    return {
        'ref_p_start_date': '2010-10-15',
        'trad_as': 'Essential Enterprises',
        'flag': True,
        'case_id': '1574ae2c-653a-4cf6-b792-798e60ddb21c',
    }

class TestMetadataValidation(IntegrationTestCase):

    def test_all_metadata_correct(self):
        # Given
        metadata = get_metadata_for_metadata_survey()

        # When
        self.launchSurvey('test', 'metadata_validation', **metadata)

        # Then
        self.assertStatusOK()
        # Assert that all the metadata is formatted in the page
        for _, value in metadata.items():
            self.assertInBody(str(value))

    def test_invalid_uuid_in_survey(self):
        # Given
        metadata = get_metadata_for_metadata_survey()
        metadata['case_id'] = 'not-a-uuid'

        # When
        self.launchSurvey('test', 'metadata_validation', **metadata)

        # Then
        # This is forbidden because it should fail to validate the metadata
        self.assertStatusForbidden()

    def test_invalid_date_in_survey(self):
        # Given
        metadata = get_metadata_for_metadata_survey()
        metadata['ref_p_start_date'] = 'not-a-date'

        # When
        self.launchSurvey('test', 'metadata_validation', **metadata)

        # Then
        # This is forbidden because it should fail to validate the metadata
        self.assertStatusForbidden()

    def test_invalid_boolean_in_survey(self):
        # Given
        metadata = get_metadata_for_metadata_survey()
        metadata['flag'] = 'not-a-bool'

        # When
        self.launchSurvey('test', 'metadata_validation', **metadata)

        # Then
        # This is forbidden because it should fail to validate the metadata
        self.assertStatusForbidden()
