import logging

from app.libs.utils import convert_tx_id
from app.metadata.metadata_store import MetaDataStore

from flask import request
from flask.ext.themes2 import render_theme_template

from flask_login import current_user

from ua_parser import user_agent_parser

logger = logging.getLogger(__name__)


def system_message(message):
    logger.debug(message)
    tx_id = None
    metadata = MetaDataStore.get_instance(current_user)
    if metadata:
        tx_id = convert_tx_id(metadata.tx_id)
    user_agent = user_agent_parser.Parse(request.headers.get('User-Agent', ''))
    return render_theme_template('default', 'system_message.html',
                                 message=message,
                                 ua=user_agent, tx_id=tx_id), message
