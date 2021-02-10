from datetime import datetime


def format_submitted_time(submitted_time):
    try:
        submitted_time = datetime.strptime(submitted_time, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        submitted_time = datetime.strptime(submitted_time, '%Y-%m-%dT%H:%M:%S')
    return submitted_time
