import wrapt
from aws_xray_sdk.core import xray_recorder
from flask import current_app


def trace():
    @wrapt.decorator
    def wrapper(wrapped, _, args, kwargs):
        # AWS X-Ray tracing

        if current_app.config['AWS_XRAY_SDK_ENABLED']:
            xray_recorder.begin_subsegment(wrapped.__name__)
            result = wrapped(*args, **kwargs)
            xray_recorder.end_subsegment()
            return result

        return wrapped(*args, **kwargs)

    return wrapper
