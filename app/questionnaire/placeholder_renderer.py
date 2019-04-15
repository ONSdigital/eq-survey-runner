from copy import deepcopy

from jsonpointer import set_pointer, resolve_pointer

from app.data_model.answer_store import AnswerStore
from app.questionnaire.placeholder_parser import PlaceholderParser


def find_pointers_containing(input_data, search_key, pointer=None):
    """
    Recursive function which lists pointers which contain a search key

    :param input_data: the input data to search
    :param search_key: the key to search for
    :param pointer: the key to search for
    :return: generator of the json pointer paths
    """
    if isinstance(input_data, dict):
        if pointer and search_key in input_data:
            yield pointer
        for k, v in input_data.items():
            if isinstance(v, dict) and search_key in v:
                yield pointer + '/' + k if pointer else '/' + k
            else:
                yield from find_pointers_containing(v, search_key, pointer + '/' + k if pointer else '/' + k)
    elif isinstance(input_data, list):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(item, search_key, '{}/{}'.format(pointer, index))


class PlaceholderRenderer:
    """
    Renders placeholders specified by a list of pointers in a schema block to their final
    strings
    """
    def __init__(self, language, answer_store=None, metadata=None):
        self.language = language
        self.answer_store = answer_store or AnswerStore()
        self.metadata = metadata
        self.placeholders = {}

    def render_pointer(self, dict_to_render, pointer_to_render):
        placeholder_parser = PlaceholderParser(language=self.language,
                                               answer_store=self.answer_store,
                                               metadata=self.metadata)

        pointer_data = resolve_pointer(dict_to_render, pointer_to_render)

        if 'text' not in pointer_data or 'placeholders' not in pointer_data:
            raise ValueError('No placeholder found at pointer')

        transformed_values = placeholder_parser.parse(pointer_data['placeholders'])

        return pointer_data['text'].format(**transformed_values)

    def render(self, dict_to_render):
        """
        Transform the current schema json to a fully rendered dictionary

        :return:
        """
        rendered_data = deepcopy(dict_to_render)
        pointer_list = find_pointers_containing(rendered_data, 'placeholders')

        for pointer in pointer_list:
            rendered_text = self.render_pointer(rendered_data, pointer)
            set_pointer(rendered_data, pointer, rendered_text)

        return rendered_data
