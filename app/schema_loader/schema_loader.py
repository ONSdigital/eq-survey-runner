import json
import logging
import os

from app import settings

import boto3

import botocore


class SchemaNotFound(Exception):
    pass

logger = logging.getLogger(__name__)


def load_schema(eq_id, form_type):
    """
    Given a schema id this method will load the correct schema file from disk. Currently the parameter is ignored
    and the MCI schema is returned
    :param eq_id: The id of the schema file
    :param form_type the form type of the file
    :return: The Schema representing in a dict
    """
    logging.debug("About to load schema for eq-id %s and form type %s", eq_id, form_type)
    # form type is mandatory JWT claim, but it isn't needed when getting schemas from the schema bucket
    # in that case default it to -1 and ignore it
    if form_type and form_type != "-1":
        schema_key = "{}_{}.json".format(eq_id, form_type)
    else:
        schema_key = "{}.json".format(eq_id)
    try:
        schema_file = open(os.path.join(settings.EQ_SCHEMA_DIRECTORY, schema_key), encoding="utf8")
        return json.load(schema_file)
    except FileNotFoundError:
        if settings.EQ_SCHEMA_BUCKET:
            try:
                s3 = boto3.resource('s3')
                schema = s3.Object(settings.EQ_SCHEMA_BUCKET, schema_key)
                jsn_schema = schema.get()['Body']
                return json.loads(jsn_schema.read().decode("utf-8"))
            except botocore.exceptions.ClientError as e:
                logging.error("S3 error: %s", e.response['Error']['Code'])
                return None
        else:
            logging.error("No file exists for eq-id %s and form type %s", eq_id, form_type)
            return None


def available_schemas():
    files = []
    available_local_schemas(files)
    if settings.EQ_SCHEMA_BUCKET:
        available_s3_schemas(files)
    return sorted(files)


def available_local_schemas(files):
    for file in os.listdir(settings.EQ_SCHEMA_DIRECTORY):
        if os.path.isfile(os.path.join(settings.EQ_SCHEMA_DIRECTORY, file)):
            # ignore hidden file
            if file.endswith(".json"):
                files.append(file)


def available_s3_schemas(files):
    try:
        s3 = boto3.resource('s3')
        schemas_bucket = s3.Bucket(settings.EQ_SCHEMA_BUCKET)
        for key in schemas_bucket.objects.all():
            files.append(key.key)
    except botocore.exceptions.ClientError as e:
        logging.error("S3 error: %s", e.response['Error']['Code'])
