from datetime import datetime

from structlog import get_logger

logger = get_logger()


def to_date(input_date_string, date_format="%Y-%m-%d"):
    formatted_date = None

    try:
        if input_date_string:
            formatted_date = datetime.strptime(input_date_string, date_format)
    except ValueError as e:
        logger.error('error parsing date string', exc_info=e, date_string=input_date_string)
    return formatted_date
