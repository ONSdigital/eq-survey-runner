from abc import ABCMeta, abstractmethod


class SchemaParser(metaclass=ABCMeta):
    '''
    Instantiates a parser with the Schema
    '''
    @abstractmethod
    def __init__(self, schema):
        raise NotImplementedError()

    '''
    Get the version of the schema parser
    '''
    @abstractmethod
    def get_parser_version(self):
        raise NotImplementedError()

    '''
    Parse the schema and return an object model, the root of which will be a
    Questionnaire object
    '''
    @abstractmethod
    def parse(self):
        raise NotImplementedError()
