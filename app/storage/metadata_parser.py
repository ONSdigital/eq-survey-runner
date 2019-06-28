import functools

from typing import Dict
from structlog import get_logger
from marshmallow import (
    Schema,
    fields,
    validate,
    EXCLUDE,
    pre_load,
    post_load,
    validates_schema,
    ValidationError,
)

from app.utilities.schema import get_schema_name_from_census_params

logger = get_logger()


class RegionCode(validate.Regexp):
    """ A region code defined as per ISO 3166-2:GB
    Currently, this does not validate the subdivision, but only checks length
    """

    def __init__(self, *args, **kwargs):
        super().__init__('^GB-[A-Z]{3}$', *args, **kwargs)


class UUIDString(fields.UUID):
    """ Currently, runner cannot handle UUID objects in metadata
    Since all metadata is serialised and deserialised to JSON.
    This custom field deserialises UUIDs to strings.
    """

    def _deserialize(self, *args, **kwargs):  # pylint: disable=arguments-differ
        return str(super()._deserialize(*args, **kwargs))


class DateString(fields.DateTime):
    """ Currently, runner cannot handle Date objects in metadata
    Since all metadata is serialised and deserialised to JSON.
    This custom field deserialises Dates to strings.
    """

    def _deserialize(self, *args, **kwargs):  # pylint: disable=arguments-differ
        return super()._deserialize(*args, **kwargs).strftime('%Y-%m-%d')


VALIDATORS = {
    'date': functools.partial(DateString, format='%Y-%m-%d', required=True),
    'uuid': functools.partial(UUIDString, required=True),
    'boolean': functools.partial(fields.Boolean, required=True),
    'string': functools.partial(fields.String, required=True),
    'url': functools.partial(fields.Url, required=True),
}


class StripWhitespaceMixin:
    @pre_load
    def strip_whitespace(self, items):  # pylint: disable=no-self-use
        for key, value in items.items():
            if isinstance(value, str):
                items[key] = value.strip()
        return items


class RunnerMetadataSchema(Schema, StripWhitespaceMixin):
    """ Metadata which is required for the operation of runner itself
    """

    jti = VALIDATORS['uuid']()
    ru_ref = VALIDATORS['string'](validate=validate.Length(min=1))
    collection_exercise_sid = VALIDATORS['string'](validate=validate.Length(min=1))
    tx_id = VALIDATORS['uuid']()
    questionnaire_id = VALIDATORS['string'](validate=validate.Length(min=1))
    response_id = VALIDATORS['string'](validate=validate.Length(min=1))
    account_service_url = VALIDATORS['url']()

    case_id = VALIDATORS['uuid'](required=False)
    account_service_log_out_url = VALIDATORS['url'](required=False)
    roles = fields.List(fields.String(), required=False)
    survey_url = VALIDATORS['url'](required=False)
    language_code = VALIDATORS['string'](required=False)

    # Either schema_name OR the three census parameters are required. Should be required after census.
    schema_name = VALIDATORS['string'](required=False)

    # The following three parameters can be removed after Census
    survey = VALIDATORS['string'](
        required=False, validate=validate.OneOf(('CENSUS', 'CCS')), missing='CENSUS'
    )
    case_type = VALIDATORS['string'](
        required=False, validate=validate.OneOf(('HH', 'HI', 'CE', 'CI'))
    )
    region_code = VALIDATORS['string'](required=False, validate=RegionCode())

    @validates_schema
    def validate_schema_name(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        """ Temporary function for census to validate the census schema parameters
        This can be removed after census.
        """
        individual_schema_claims = (
            data.get('survey'),
            data.get('case_type'),
            data.get('region_code'),
        )
        if not data.get('schema_name'):
            if not all(individual_schema_claims):
                raise ValidationError(
                    "Either 'schema_name' or 'survey' and 'case_type' and 'region_code' must be defined"
                )

    @post_load
    def convert_schema_name(self, data, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        """ Temporary function for census to transform parameters into a census schema
        This can be removed after census.
        """
        if data.get('schema_name'):
            logger.info(
                f'Ignoring claims: survey: {data.get("survey")}, case_type: {data.get("case_type")} because schema_name was specified'
            )
            data.pop('survey', None)
            data.pop('case_type', None)
        else:
            data['schema_name'] = get_schema_name_from_census_params(
                data.get('survey'), data.get('case_type'), data.get('region_code')
            )
        return data


def validate_questionnaire_claims(claims, questionnaire_specific_metadata):
    """ Validate any survey specific claims required for a questionnaire"""
    dynamic_fields = {}

    for metadata_field in questionnaire_specific_metadata:
        field_arguments = {}
        validators = []

        if metadata_field.get('optional'):
            field_arguments['required'] = False

        if any(
            length_limit in metadata_field
            for length_limit in ('min_length', 'max_length', 'length')
        ):
            validators.append(
                validate.Length(
                    min=metadata_field.get('min_length'),
                    max=metadata_field.get('max_length'),
                    equal=metadata_field.get('length'),
                )
            )

        dynamic_fields[metadata_field['name']] = VALIDATORS[metadata_field['type']](
            validate=validators, **field_arguments
        )

    questionnaire_metadata_schema = type(
        'QuestionnaireMetadataSchema', (Schema, StripWhitespaceMixin), dynamic_fields
    )(unknown=EXCLUDE)

    # The load method performs validation.
    return questionnaire_metadata_schema.load(claims)


def validate_runner_claims(claims: Dict):
    """ Validate claims required for runner to function"""
    runner_metadata_schema = RunnerMetadataSchema(unknown=EXCLUDE)
    return runner_metadata_schema.load(claims)
