import re
from functools import wraps

from flask import current_app, g, session as cookie_session, render_template as flask_render_template
from structlog import get_logger

from app.globals import get_session_timeout_in_seconds

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
    template = '{}.html'.format(template).lower()

    return flask_render_template(
        template,
        survey_title=safe_content(g.schema.json['title']),
        account_service_url=cookie_session.get('account_service_url'),
        account_service_log_out_url=cookie_session.get('account_service_log_out_url'),
        survey_id=g.schema.json['survey_id'],
        **kwargs
    )


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
