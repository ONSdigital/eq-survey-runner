from app.questionnaire.rules import evaluate_when_rules


def get_question_title(question_schema, answer_store, schema, metadata):
    """Return the value that should be used as the title to a question
    May be from question.title or question.titles"""

    if question_schema.get('title') is not None:
        return question_schema['title']

    titles = question_schema.get('titles')

    return get_title_from_titles(metadata, schema, answer_store, titles)


def get_title_from_titles(metadata, schema, answer_store, titles):
    """returns a title from titles available by evaluating the when rules , if all fail returns default"""
    for when, value in ((title['when'], title['value']) for title in titles if 'when' in title):
        if evaluate_when_rules(when, schema, metadata, answer_store):
            return value
    return titles[-1]['value']
