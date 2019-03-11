from app.data_model.answer_store import AnswerStore
from app.questionnaire.placeholder_transforms import PlaceholderTransforms


class PlaceholderParser:
    """
    Parses placeholder statements from a schema dict and returns a map of their
    final values
    """
    def __init__(self, answer_store=None, metadata=None):
        self._answer_store = answer_store or AnswerStore()
        self._metadata = metadata
        self._transformer = PlaceholderTransforms()

    def _lookup_answer(self, answer_id):
        found_answers = self._answer_store.filter(answer_ids=[answer_id])

        if found_answers.count() > 0:
            return found_answers.values()[0]

    def parse(self, placeholder_list):
        placeholder_map = {}

        for placeholder in placeholder_list:
            placeholder_id = placeholder['placeholder']

            if 'value' in placeholder:
                source_id = placeholder['value']['identifier']

                if placeholder['value']['source'] == 'answers':
                    placeholder_map[placeholder_id] = self._lookup_answer(source_id)
                elif placeholder['value']['source'] == 'metadata':
                    placeholder_map[placeholder_id] = self._metadata[source_id]
            elif 'transforms' in placeholder:
                placeholder_map[placeholder_id] = self.parse_transforms(placeholder['transforms'])

        return placeholder_map

    def parse_transforms(self, transform_list):
        transformed_value = None

        for transform in transform_list:
            transform_args = {}
            for arg_key, arg_value in transform['arguments'].items():
                if 'value' in arg_value:
                    transform_args[arg_key] = arg_value['value']
                elif 'source' not in arg_value:
                    transform_args[arg_key] = arg_value
                elif arg_value['source'] == 'answers':
                    if isinstance(arg_value['identifier'], list):
                        transform_args[arg_key] = [self._lookup_answer(identifier) for identifier in arg_value['identifier']]
                    else:
                        transform_args[arg_key] = self._lookup_answer(arg_value['identifier'])
                elif arg_value['source'] == 'metadata':
                    transform_args[arg_key] = self._metadata[arg_value['identifier']]
                elif arg_value['source'] == 'previous_transform':
                    transform_args[arg_key] = transformed_value

            transformed_value = getattr(self._transformer, transform['transform'])(**transform_args)

        return transformed_value
