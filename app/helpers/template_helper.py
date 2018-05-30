from flask import current_app, g
from flask_login import current_user
from flask_themes2 import render_theme_template
from structlog import get_logger

from app.globals import get_metadata
from app.templating.metadata_context import build_metadata_context
from app.templating.template_renderer import TemplateRenderer

logger = get_logger()


def with_session_timeout(func):
    def session_wrapper(*args, **kwargs):
        session_timeout = current_app.config['EQ_SESSION_TIMEOUT_SECONDS']
        schema_session_timeout = g.schema.json.get('session_timeout_in_seconds')
        if schema_session_timeout is not None and \
           schema_session_timeout < current_app.config['EQ_SESSION_TIMEOUT_SECONDS']:
            session_timeout = schema_session_timeout

        session_timeout_prompt = g.schema.json.get('session_prompt_in_seconds') or \
            current_app.config['EQ_SESSION_TIMEOUT_PROMPT_SECONDS']

        return func(
            *args,
            session_timeout=session_timeout,
            session_timeout_prompt=session_timeout_prompt,
            **kwargs
        )

    return session_wrapper


def with_metadata(func):
    def metadata_wrapper(*args, **kwargs):
        metadata = get_metadata(current_user)
        metadata_context = build_metadata_context(metadata)

        return func(*args, metadata=metadata_context, **kwargs)

    return metadata_wrapper


def with_analytics(func):
    def analytics_wrapper(*args, **kwargs):
        return func(*args, analytics_ua_id=current_app.config['EQ_UA_ID'], **kwargs)

    return analytics_wrapper


def with_questionnaire_url_prefix(func):
    def url_prefix_wrapper(*args, **kwargs):
        metadata = get_metadata(current_user)
        metadata_context = build_metadata_context(metadata)

        url_prefix = '/questionnaire/{}/{}/{}'.format(
            metadata_context['eq_id'],
            metadata_context['form_type'],
            metadata_context['collection_id'],
        )

        return func(*args, url_prefix=url_prefix, **kwargs)

    return url_prefix_wrapper


def with_legal_basis(func):
    def legal_basis_wrapper(*args, **kwargs):
        return func(*args, legal_basis=g.schema.json['legal_basis'], **kwargs)

    return legal_basis_wrapper


def render_template(template, **kwargs):
    theme = g.schema.json.get('theme')
    template = '{}.html'.format(template).lower()

    return render_theme_template(
        theme,
        template,
        survey_title=TemplateRenderer.safe_content(g.schema.json['title']),
        survey_id=g.schema.json['survey_id'],
        **kwargs
    )
