from functools import wraps
from opencensus.trace import execution_context


def capture_trace(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        tracer = execution_context.get_opencensus_tracer()
        with tracer.span(name=f.__name__) as span:  # noqa: F841
            return f(*args, **kwargs)

    return decorated_function
