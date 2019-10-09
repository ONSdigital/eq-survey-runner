from app.helpers import get_span_and_trace


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def cloud_trace_header():
    header = AttrDict()
    header.update(
        {'headers': {'X-Cloud-Trace-Context': '0123456789/0123456789012345678901;o=1'}}
    )
    return header


def test_get_span_and_trace():
    header = cloud_trace_header()
    span, trace = get_span_and_trace(header.headers)  # pylint: disable=no-member
    assert trace == '0123456789'
    assert span == '0123456789012345678901'


def test_get_span_and_trace_no_xcloud_header():
    header = cloud_trace_header()
    del header.headers['X-Cloud-Trace-Context']  # pylint: disable=no-member
    span, trace = get_span_and_trace(header.headers)  # pylint: disable=no-member

    assert trace is None
    assert span is None


def test_get_span_and_trace_malformed_xcloud_header():  # pylint: disable=no-member
    header = cloud_trace_header()
    header.headers[
        'X-Cloud-Trace-Context'
    ] = 'not a real trace context'  # pylint: disable=no-member
    span, trace = get_span_and_trace(header.headers)  # pylint: disable=no-member
    assert trace is None
    assert span is None
