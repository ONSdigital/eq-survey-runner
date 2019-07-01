from copy import deepcopy

import pytest
from marshmallow import ValidationError

from app.storage.metadata_parser import (
    validate_runner_claims,
    validate_questionnaire_claims,
)
from app.utilities.schema import transform_region_code, transform_case_type


def test_spaces_are_stripped_from_string_fields(fake_metadata_runner):
    fake_metadata_runner['collection_exercise_sid'] = '  stripped     '

    output = validate_runner_claims(fake_metadata_runner)

    assert output['collection_exercise_sid'] == 'stripped'


def test_empty_strings_are_not_valid(fake_metadata_runner):
    fake_metadata_runner['schema_name'] = ''

    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


def test_validation_does_not_change_metadata(
    fake_metadata_full, fake_questionnaire_metadata_requirements_full
):
    fake_metadata_copy = deepcopy(fake_metadata_full)
    validate_questionnaire_claims(
        fake_metadata_full, fake_questionnaire_metadata_requirements_full
    )

    assert fake_metadata_full == fake_metadata_copy


def test_validation_no_error_when_optional_field_not_passed(fake_metadata_runner):
    field_specification = [
        {'name': 'optional_field', 'type': 'string', 'optional': True}
    ]

    validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_validation_field_required_by_default(fake_metadata_runner):
    field_specification = [{'name': 'required_field', 'type': 'string'}]

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_minimum_length(fake_metadata_runner):
    field_specification = [{'name': 'some_field', 'type': 'string', 'min_length': 5}]

    fake_metadata_runner['some_field'] = '123456'

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '1'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_maximum_length(fake_metadata_runner):
    field_specification = [{'name': 'some_field', 'type': 'string', 'max_length': 5}]

    fake_metadata_runner['some_field'] = '1234'

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '123456'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_min_and_max_length(fake_metadata_runner):
    field_specification = [
        {'name': 'some_field', 'type': 'string', 'min_length': 4, 'max_length': 5}
    ]

    fake_metadata_runner['some_field'] = '1234'

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '123456'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '123'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_length_equals(fake_metadata_runner):
    field_specification = [{'name': 'some_field', 'type': 'string', 'length': 4}]

    fake_metadata_runner['some_field'] = '1234'

    validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '123456'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)

    fake_metadata_runner['some_field'] = '123'

    with pytest.raises(ValidationError):
        validate_questionnaire_claims(fake_metadata_runner, field_specification)


def test_uuid_deserialisation(fake_metadata_runner):
    claims = validate_runner_claims(fake_metadata_runner)

    assert isinstance(claims['tx_id'], str)


def test_unknown_claims_are_not_deserialised(fake_metadata_runner):
    fake_metadata_runner['unknown_key'] = 'some value'
    claims = validate_runner_claims(fake_metadata_runner)
    assert 'unknown_key' not in claims


def test_minimum_length_on_runner_metadata(fake_metadata_runner):
    validate_runner_claims(fake_metadata_runner)

    fake_metadata_runner['schema_name'] = ''
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_metadata_runner)


def test_deserialisation_iso_8601_dates(fake_metadata_runner):
    """ Runner cannot currently handle date objects in metadata"""
    field_specification = [{'name': 'birthday', 'type': 'date'}]

    fake_metadata_runner['birthday'] = '2019-11-1'
    claims = validate_questionnaire_claims(fake_metadata_runner, field_specification)

    assert isinstance(claims['birthday'], str)


def test_census_params_without_schema_name(fake_census_metadata_runner):
    claims = validate_runner_claims(fake_census_metadata_runner)

    assert claims['schema_name'] == 'census_individual_gb_eng'


def test_case_type_transform():
    assert transform_case_type('HI') == 'individual'
    assert transform_case_type('HH') == 'household'
    assert transform_case_type('CE') == 'communal_establishment'
    assert transform_case_type('CI') == 'communal_individual'

    with pytest.raises(KeyError):
        transform_case_type('household')

    with pytest.raises(KeyError):
        transform_case_type('BAD')


@pytest.mark.parametrize(
    'test_input, expected',
    [('GB-ENG', 'gb_eng'), ('GB-WLS', 'gb_wls'), ('GB-NIR', 'gb_nir')],
)
def test_region_code_is_lower_cased_and_underscored(test_input, expected):
    assert transform_region_code(test_input) == expected


def test_survey_parameter_defaults_to_census(fake_census_metadata_runner):
    del fake_census_metadata_runner['survey']
    claims = validate_runner_claims(fake_census_metadata_runner)

    assert claims['schema_name'] == 'census_individual_gb_eng'


def test_survey_parameter_allows_ccs(fake_census_metadata_runner):
    fake_census_metadata_runner['survey'] = 'CCS'
    claims = validate_runner_claims(fake_census_metadata_runner)

    assert claims['schema_name'] == 'ccs_individual_gb_eng'


def test_bad_survey_parameter(fake_census_metadata_runner):
    fake_census_metadata_runner['survey'] = 'bad_survey'
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_census_metadata_runner)


def test_bad_case_type_parameter(fake_census_metadata_runner):
    fake_census_metadata_runner['case_type'] = 'bad_case_type'
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_census_metadata_runner)


def test_bad_region_code_parameter(fake_census_metadata_runner):
    fake_census_metadata_runner['region_code'] = 'bad_region_code'
    with pytest.raises(ValidationError):
        validate_runner_claims(fake_census_metadata_runner)


def test_no_census_params_and_no_schema_name_raises_error(fake_census_metadata_runner):
    fake_census_metadata_runner.pop('schema_name', None)
    fake_census_metadata_runner.pop('region_code', None)
    fake_census_metadata_runner.pop('case_type', None)
    fake_census_metadata_runner.pop('survey', None)

    with pytest.raises(ValidationError):
        validate_runner_claims(fake_census_metadata_runner)
