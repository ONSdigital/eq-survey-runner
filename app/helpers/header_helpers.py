def get_span_and_trace(headers):
    try:
        trace, span = headers.get('X-Cloud-Trace-Context').split('/')
    except (ValueError, AttributeError):
        return None, None

    span = span.split(';')[0]
    return span, trace
