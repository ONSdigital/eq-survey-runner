from flask import g, request
from flask_babel import get_locale
from flask_login import current_user

from app.globals import get_metadata, get_session_store
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.utilities.schema import get_allowed_languages

# en_US has been used for Ulstér Scotch as there is no language code in the
# CLDR (http://cldr.unicode.org) for it and this is required for survey runner
# to work (http://babel.pocoo.org/en/latest/locale.html).

LANGUAGE_TEXT = {
    'en': 'English',
    'cy': 'Cymraeg',
    'ga': 'Gaeilge',
    'en_US': 'Ulstér Scotch',
}


def handle_language():
    session_store = get_session_store()
    if session_store:
        launch_language = _get_launch_language()
        g.allowed_languages = get_allowed_languages(
            session_store.session_data.schema_name, launch_language
        )

        request_language = request.args.get('language_code')
        if request_language and request_language in g.allowed_languages:
            session_store.session_data.language_code = request_language
            session_store.save()


def get_languages_context():
    context = []
    allowed_languages = g.get('allowed_languages')
    if allowed_languages and len(allowed_languages) > 1:
        for language in allowed_languages:
            context.append(_get_language_context(language))
        return {'languages': context}
    return None


def _get_language_context(language_code):
    return {
        'ISOCode': language_code,
        'url': '?language_code=' + language_code,
        'text': LANGUAGE_TEXT.get(language_code),
        'current': language_code == str(get_locale()),
    }


def _get_launch_language():
    metadata = get_metadata(current_user)
    if metadata:
        return metadata['language_code']
    return DEFAULT_LANGUAGE_CODE
