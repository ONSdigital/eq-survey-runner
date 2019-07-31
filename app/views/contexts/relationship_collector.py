from app.questionnaire.placeholder_transforms import PlaceholderTransforms


# This is required until we can resolve placeholders for list items in schema.
def transform_relationships(block, answer_store, location):
    transform = PlaceholderTransforms('en')
    first_person_name = _get_name(answer_store, location.from_list_item_id)
    second_person_name = _get_name(answer_store, location.to_list_item_id)
    first_person_name_possessive = transform.format_possessive(first_person_name)

    placeholders = {
        'first_person_name': first_person_name,
        'second_person_name': second_person_name,
        'first_person_name_possessive': first_person_name_possessive,
    }

    question = block['question']
    question['title'] = question['title'].format(**placeholders)
    answer = question['answers'][0]
    answer['playback'] = answer['playback'].format(**placeholders)

    for option in answer['options']:
        option['title'] = option['title'].format(**placeholders)
        option['playback'] = option['playback'].format(**placeholders)

    return block


def _get_name(answer_store, list_item_id):
    name = []
    answers = answer_store.get_answers_by_answer_id(
        answer_ids=['first-name', 'last-name'], list_item_id=list_item_id
    )
    for answer in answers:
        name.append(answer.value.strip())

    return ' '.join(name)
