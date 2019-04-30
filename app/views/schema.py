from os import listdir
from os.path import isfile, join

from quart import Blueprint, jsonify
from app.utilities.schema import load_schema_from_params

schema_blueprint = Blueprint('schema', __name__)


@schema_blueprint.route('/schemas/<eq_id>/<form_type>', methods=['GET'])
def get_schema_json(eq_id, form_type):
    try:
        schema = load_schema_from_params(eq_id, form_type)

        return jsonify(schema.json)
    except FileNotFoundError:
        return 'Schema Not Found', 404


@schema_blueprint.route('/schemas', methods=['GET'])
def list_schemas():
    schema_path = 'data/en'
    onlyfiles = [f for f in listdir(schema_path) if isfile(join(schema_path, f)) and f.endswith('.json')]

    return jsonify(onlyfiles)
