import pytest
from app.utilities.schema import get_schema_name_from_census_params


def test_transform_schema_name_good_scenarios():
    assert (
        get_schema_name_from_census_params('census', 'HI', 'GB-WLS')
        == 'census_individual_gb_wls'
    )
    assert (
        get_schema_name_from_census_params('census', 'HH', 'GB-WLS')
        == 'census_household_gb_wls'
    )
    assert (
        get_schema_name_from_census_params('census', 'CE', 'GB-WLS')
        == 'census_communal_establishment_gb_wls'
    )
    assert (
        get_schema_name_from_census_params('census', 'CI', 'GB-WLS')
        == 'census_communal_individual_gb_wls'
    )


def test_transform_schema_name_bad_case_type_raises_error():
    with pytest.raises(ValueError):
        get_schema_name_from_census_params('census', 'bad', 'GB-WLS')
