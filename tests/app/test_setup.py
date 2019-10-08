import pytest

from app.helpers import get_span_and_trace


def test_get_span_and_trace(header):
    span, trace = get_span_and_trace(header)
    assert trace == '0123456789'
    assert span == '0123456789012345678901'


def test_get_span_and_trace_no_xcloud_header(header):
    del header.headers['X-Cloud-Trace-Context']
    span, trace = get_span_and_trace(header)
    assert trace == ' '
    assert span == ' '

def test_get_span_and_trace_malformed_xcloud_header(header):
    header.headers['X-Cloud-Trace-Context'] = 'not a real trace context'
    span, trace = get_span_and_trace(header)
    assert trace == ' '
    assert span == ' '
