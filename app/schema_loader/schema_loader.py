import json


class SchemaLoader(object):

    def load_schema(self, schema_id):
        schema_file = open("surveys/mci.json")
        return json.load(schema_file)
