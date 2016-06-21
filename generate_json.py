import json
import os.path
from app.parser.schema_parser_factory import SchemaParserFactory
import logging

logger = logging.getLogger(__name__)

JSON_PATH = 'app/data/'
PYTHON_MODEL_PATH = 'app/surveys'


def convert_to_json(questionnaire):
    # Format the Json output
    json_str = json.dumps(questionnaire.to_json(), sort_keys=True, indent=4)
    return json_str


def parse_schema(json_survey):
    # Check the generated json parses successfully
    parser = SchemaParserFactory.create_parser(json.loads(json_survey))
    return parser.parse()


def generate_json_survey(python_model):
    # Import the required module and convert the python model to json format
    module = __import__('app.surveys.' + python_model, globals(), locals(), [python_model, 'form_type'])
    model = eval("module." + python_model)
    file_name = model.eq_id + "_" + module.form_type
    json_survey = convert_to_json(model)
    return json_survey, file_name


def write_json_to_file(json_name, json_survey):
    try:
        path = os.path.join(JSON_PATH, json_name + ".json")
        f = open(path, "w")
        f.write(json_survey)
        f.close()

    except IOError as e:
        logger.error("Error creating json file")
        logger.exception(e)


def generate_all_json():
    # Loop through all the files in the survey folder, generating json for each, before writing to disk
    for filename in os.listdir(PYTHON_MODEL_PATH):
        if filename.endswith('.py') and not filename.startswith('_'):
            python_model = os.path.splitext(filename)[0]
            json_survey, file_name = generate_json_survey(python_model)
            parse_schema(json_survey)
            write_json_to_file(file_name, json_survey)

if __name__ == '__main__':
    generate_all_json()
