import json


class SchemaLoader(object):

    def __init__(self, location):
      self.location = location

    def load_schema(self, schema_id):
        schema_file = open(self.location + "/mci.json")
        return json.load(schema_file)
