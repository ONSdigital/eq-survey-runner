import json
import logging
import os

from app import settings

import boto3

import botocore


class SchemaNotFound(Exception):
    pass

logger = logging.getLogger(__name__)


def load_schema(eq_id, form_type, language_code='en'):
    """
    Given a schema id this method will load the correct schema file from disk. Currently the parameter is ignored
    and the MCI schema is returned
    :param eq_id: The id of the schema file
    :param form_type the form type of the file
    :param language_code the language of the schema to load
    :return: The Schema representing in a dict
    """
    logging.debug("About to load schema for eq-id %s and form type %s and language %s", eq_id, form_type, language_code)

    filename_format = "{}.json"

    if form_type and form_type != "-1":
        filename_format = "{}_" + filename_format

    if language_code and language_code != "en":
        filename_format = "{}_" + filename_format

    # form type is mandatory JWT claim, but it isn't needed when getting schemas from the schema bucket
    # in that case default it to -1 and ignore it
    if form_type and form_type != "-1":
        return load_schema_file(filename_format.format(eq_id, form_type, language_code))

    return load_s3_schema_file("{}.json".format(eq_id))


def load_s3_schema_file(schema_file):
    if settings.EQ_SCHEMA_BUCKET:
        try:
            s3 = boto3.resource('s3')
            schema = s3.Object(settings.EQ_SCHEMA_BUCKET, schema_file)
            jsn_schema = schema.get()['Body']
            return json.loads(jsn_schema.read().decode("utf-8"))
        except botocore.exceptions.ClientError as e:
            logging.error("S3 error: %s", e.response['Error']['Code'])
    return None


def load_schema_file(schema_file):
    try:
        schema_path = os.path.join(settings.EQ_SCHEMA_DIRECTORY, schema_file)
        with open(schema_path, encoding="utf8") as json_data:
            return json.load(json_data)
    except FileNotFoundError:
        logging.error("No schema file exists %s", schema_file)
        return None


def available_schemas():
    files = available_local_schemas()
    if settings.EQ_SCHEMA_BUCKET:
        files.extend(available_s3_schemas())
    return sorted(files)


def available_local_schemas():
    files = []
    for file in os.listdir(settings.EQ_SCHEMA_DIRECTORY):
        if os.path.isfile(os.path.join(settings.EQ_SCHEMA_DIRECTORY, file)):
            # ignore hidden file
            if file.endswith(".json"):
                files.append(file)
    return files


def available_s3_schemas():
    files = []
    try:
        s3 = boto3.resource('s3')
        schemas_bucket = s3.Bucket(settings.EQ_SCHEMA_BUCKET)
        for key in schemas_bucket.objects.all():
            files.append(key.key)
    except botocore.exceptions.ClientError as e:
        logging.error("S3 error: %s", e.response['Error']['Code'])
    return files
