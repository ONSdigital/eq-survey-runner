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
        if search_key in input_data:
            yield pointer or ''
        for k, v in input_data.items():
            if isinstance(v, dict) and search_key in v:
                yield pointer + '/' + k if pointer else '/' + k
            else:
                yield from find_pointers_containing(
                    v, search_key, pointer + '/' + k if pointer else '/' + k
                )
    elif isinstance(input_data, list):
        for index, item in enumerate(input_data):
            yield from find_pointers_containing(
                item, search_key, '{}/{}'.format(pointer, index)
            )


class PlaceholderRenderer:
    """
    Renders placeholders specified by a list of pointers in a schema block to their final
    strings
    """

    def __init__(
        self, language, schema, answer_store=None, metadata=None
    ):
        self._language = language
        self._schema = schema
        self._answer_store = answer_store or AnswerStore()
        self._metadata = metadata

    def render_pointer(self, dict_to_render, pointer_to_render, list_item_id):
        pointer_data = resolve_pointer(dict_to_render, pointer_to_render)

        return self.render_placeholder(pointer_data, list_item_id)

    def render_placeholder(self, placeholder_data, list_item_id):
        placeholder_parser = PlaceholderParser(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            metadata=self._metadata,
            list_item_id=list_item_id,
        )

        if 'text' not in placeholder_data or 'placeholders' not in placeholder_data:
            raise ValueError('No placeholder found to render')

        transformed_values = placeholder_parser.parse(placeholder_data['placeholders'])

        return placeholder_data['text'].format(**transformed_values)

    def render(self, dict_to_render, list_item_id):
        """
        Transform the current schema json to a fully rendered dictionary
        """
        rendered_data = deepcopy(dict_to_render)
        pointer_list = find_pointers_containing(rendered_data, 'placeholders')

        for pointer in pointer_list:
            rendered_text = self.render_pointer(rendered_data, pointer, list_item_id)
            set_pointer(rendered_data, pointer, rendered_text)

        return rendered_data
