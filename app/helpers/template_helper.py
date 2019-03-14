from functools import wraps

from flask import current_app, g, session as cookie_session
from flask_login import current_user
from flask_themes2 import render_theme_template
from structlog import get_logger

from app.globals import get_metadata, get_session_timeout_in_seconds
from app.templating.metadata_context import build_metadata_context
from app.templating.template_renderer import TemplateRenderer

logger = get_logger()


def with_session_timeout(func):
    @wraps(func)
    def session_wrapper(*args, **kwargs):
        session_timeout = get_session_timeout_in_seconds(g.schema)

        return func(
            *args,
            session_timeout=session_timeout,
            **kwargs
        )

    return session_wrapper


def with_metadata_context(func):
    @wraps(wraps)
    def metadata_context_wrapper(*args, **kwargs):
        metadata = get_metadata(current_user)
        metadata_context = build_metadata_context(metadata)

        return func(*args, metadata_context=metadata_context, **kwargs)

    return metadata_context_wrapper


def with_analytics(func):
    @wraps(func)
    def analytics_wrapper(*args, **kwargs):
        return func(*args, analytics_ua_id=current_app.config['EQ_UA_ID'], **kwargs)

    return analytics_wrapper


def with_legal_basis(func):
    @wraps(func)
    def legal_basis_wrapper(*args, **kwargs):
        legal_basis = g.schema.json.get('legal_basis')
        return func(*args, legal_basis=legal_basis, **kwargs)
    return legal_basis_wrapper


def render_template(template, **kwargs):
    theme = g.schema.json.get('theme')
    template = '{}.html'.format(template).lower()

    return render_theme_template(
        theme,
        template,
        survey_title=TemplateRenderer.safe_content(g.schema.json['title']),
        account_service_url=cookie_session.get('account_service_url'),
        account_service_log_out_url=cookie_session.get('account_service_log_out_url'),
        survey_id=g.schema.json['survey_id'],
        **kwargs
    )
