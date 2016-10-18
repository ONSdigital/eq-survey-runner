import logging

from datetime import datetime

logger = logging.getLogger(__name__)


def to_date(input_date_string, date_format="%Y-%m-%d"):
    formatted_date = None

    try:
        if input_date_string:
            formatted_date = datetime.strptime(input_date_string, date_format)
    except ValueError as e:
        logger.exception(e)
        logger.error("Error parsing date string for %s", input_date_string)
    return formatted_date
