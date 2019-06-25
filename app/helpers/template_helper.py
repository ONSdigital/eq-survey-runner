import re

from flask import (
    current_app,
    session as cookie_session,
    render_template as flask_render_template,
)


def render_template(template, **kwargs):
    template = f'{template.lower()}.html'

    return flask_render_template(
        template,
        account_service_url=cookie_session.get('account_service_url'),
        account_service_log_out_url=cookie_session.get('account_service_log_out_url'),
        google_tag_manager_id=current_app.config['EQ_GOOGLE_TAG_MANAGER_ID'],
        google_tag_manager_auth=current_app.config['EQ_GOOGLE_TAG_MANAGER_AUTH'],
        google_tag_manager_preview=current_app.config['EQ_GOOGLE_TAG_MANAGER_PREVIEW'],
        **kwargs,
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
