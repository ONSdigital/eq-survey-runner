from app.helpers import get_span_and_trace


def cloud_trace_header():
    return {'X-Cloud-Trace-Context': '0123456789/0123456789012345678901;o=1'}


def test_get_span_and_trace():
    header = cloud_trace_header()
    span, trace = get_span_and_trace(header)  # pylint: disable=no-member
    assert trace == '0123456789'
    assert span == '0123456789012345678901'


def test_get_span_and_trace_no_xcloud_header():
    header = cloud_trace_header()
    del header['X-Cloud-Trace-Context']  # pylint: disable=no-member
    span, trace = get_span_and_trace(header)  # pylint: disable=no-member

    assert trace is None
    assert span is None


def test_get_span_and_trace_malformed_xcloud_header():  # pylint: disable=no-member
    header = cloud_trace_header()
    header['X-Cloud-Trace-Context'] = 'not a real trace context'
    span, trace = get_span_and_trace(header)  # pylint: disable=no-member
    assert trace is None
    assert span is None
