from jinja2 import escape


def build_schema_context(metadata, collection_metadata, schema, answer_store, answer_ids_on_path):
    """
    Build questionnaire schema context containing exercise and answers
    :param metadata: user metadata
    :param collection_metadata: metadata for the collection of the questionnaire
    :param schema: Survey schema
    :param answer_store: all the answers for the given questionnaire
    :param answer_ids_on_path: a list of the answer ids on the routing path
    :return: questionnaire schema context
    """
    return {
        'metadata': build_schema_metadata(metadata, schema),
        'collection_metadata': collection_metadata,
        'answers': _build_answers(answer_store, answer_ids_on_path),
    }


def _build_answers(answer_store, answer_ids_on_path):
    answers = {}

    for answer_id in answer_ids_on_path:

        matching_answers = answer_store.filter(answer_ids=[answer_id])

        if matching_answers:
            value = json_and_html_safe(next(iter(matching_answers))['value'])
        else:
            value = ''

        answers[answer_id] = value

    return answers


def build_schema_metadata(metadata, schema):
    schema_metadata = schema.json['metadata']
    parsed = {metadata_field['name']: json_and_html_safe(metadata[metadata_field['name']])
              for metadata_field in schema_metadata if metadata_field['name'] in metadata}

    return parsed


def json_and_html_safe(data):
    if data and isinstance(data, str):
        return escape(data.replace('\\', r'\\'))
    return data
