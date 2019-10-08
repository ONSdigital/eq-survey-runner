def get_span_and_trace(request):
    trace, span = request.headers.get('X-Cloud-Trace-Context', ' / ').split('/')
    span = span.split(';')[0]
    return span, trace

