def get_introduction_context(schema_json):
    """
    :param schema_json: the schema for the current questionnaire
    :return: introduction context
    """
    introduction = schema_json['introduction']

    return {
        "title": schema_json['title'],
        "survey_code": schema_json['survey_id'],
        "description": _get_description(introduction),
        "information_to_provide": _get_info_to_provide(introduction),
    }


def _get_info_to_provide(introduction):
    if introduction and introduction.get('information_to_provide') is not None:
        return introduction['information_to_provide']

    return None


def _get_description(introduction):
    if introduction and introduction['description']:
        return introduction['description']

    return None
