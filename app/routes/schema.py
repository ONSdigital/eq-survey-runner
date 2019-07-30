from os import listdir
from os.path import isfile, join

from flask import Blueprint, jsonify
from app.utilities.schema import load_schema_from_name

schema_blueprint = Blueprint('schema', __name__)


@schema_blueprint.route('/schemas/<schema_name>', methods=['GET'])
def get_schema_json_from_name(schema_name):
    try:
        schema = load_schema_from_name(schema_name)
        return jsonify(schema.json)
    except FileNotFoundError:
        return 'Schema Not Found', 404


@schema_blueprint.route('/schemas', methods=['GET'])
def list_schemas():
    schema_path = 'data/en'
    schema_names = [
        f.replace('.json', '')
        for f in listdir(schema_path)
        if isfile(join(schema_path, f)) and f.endswith('.json')
    ]

    return jsonify(schema_names)
