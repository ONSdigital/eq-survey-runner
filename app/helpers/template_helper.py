import re

from flask import (
    current_app,
    session as cookie_session,
    render_template as flask_render_template,
    request,
)
from flask_babel import get_locale, lazy_gettext

from app.setup import cache
from app.helpers.language_helper import get_languages_context


@cache.memoize()
def get_page_header_context(language, theme):
    default_context = {
        'logo': 'ons-logo-pos-' + language,
        'logoAlt': lazy_gettext('Office for National Statistics logo'),
    }
    context = {
        'default': default_context,
        'social': default_context,
        'northernireland': default_context,
        'census': {
            **default_context,
            'titleLogo': '/img/census-logo-' + language + '.svg',
            'titleLogoAlt': lazy_gettext('Census 2021'),
        },
        'census-nisra': {
            'logo': 'nisra-logo-en',
            'logoAlt': lazy_gettext(
                'Northern Ireland Statistics and Research Agency logo'
            ),
            'titleLogo': '/img/census-logo-en.svg',
            'titleLogoAlt': lazy_gettext('Census 2021'),
        },
    }
    return context.get(theme)


def _map_theme(theme):
    """ Maps a survey schema theme to a design system theme

    :param theme: A schema defined theme
    :returns: A design system theme
    """
    if theme and theme not in ['census', 'census-nisra']:
        return 'main'
    return 'census'


def render_template(template, **kwargs):
    template = f'{template.lower()}.html'

    page_header_context = get_page_header_context(
        get_locale().language, cookie_session.get('theme', 'census')
    )
    page_header_context.update({'title': cookie_session.get('survey_title')})

    google_tag_mananger_context = get_google_tag_mananger_context()

    return flask_render_template(
        template,
        account_service_url=cookie_session.get('account_service_url'),
        account_service_log_out_url=cookie_session.get('account_service_log_out_url'),
        cookie_settings_url=current_app.config['COOKIE_SETTINGS_URL'],
        page_header=page_header_context,
        theme=_map_theme(cookie_session.get('theme')),
        languages=get_languages_context(),
        schema_theme=cookie_session.get('theme'),
        language_code=get_locale().language,
        survey_title=cookie_session.get('survey_title'),
        **google_tag_mananger_context,
        **kwargs,
    )


def get_google_tag_mananger_context():
    cookie = request.cookies.get('ons_cookie_policy')
    if cookie and "\'usage\':true" in cookie:
        return {
            'google_tag_manager_id': current_app.config['EQ_GOOGLE_TAG_MANAGER_ID'],
            'google_tag_manager_auth': current_app.config['EQ_GOOGLE_TAG_MANAGER_AUTH'],
            'google_tag_manager_preview': current_app.config[
                'EQ_GOOGLE_TAG_MANAGER_PREVIEW'
            ],
        }
    return {}


def safe_content(content):
    """Make content safe.

    Replaces variable with ellipsis and strips any HTML tags.

    :param (str) content: Input string.
    :returns (str): Modified string.
    """
    if content is not None:
        # Replace piping with ellipsis
        content = re.sub(r'{.*?}', '…', content)
        # Strip HTML Tags
        content = re.sub(r'</?[^>]+>', '', content)
    return content
