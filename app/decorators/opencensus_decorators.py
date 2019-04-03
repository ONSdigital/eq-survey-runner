from functools import wraps
from opencensus.trace import execution_context


def capture_trace(function_to_wrap):
    @wraps(function_to_wrap)
    def decorated_function(*args, **kwargs):
        tracer = execution_context.get_opencensus_tracer()
        with tracer.span(name=function_to_wrap.__name__):
            return function_to_wrap(*args, **kwargs)

    return decorated_function
