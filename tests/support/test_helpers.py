import json
import datetime
from hamcrest.core.base_matcher import BaseMatcher
import os
import pytz


class IsResponseWithStatus(BaseMatcher):
    def __init__(self, expected_status):
        self.expected_status = expected_status

    def _matches(self, response):
        return response.status_code == self.expected_status

    def describe_to(self, description):
        description.append_text(
            "response with status code %d" % self.expected_status)


def has_status(status_code):
    return IsResponseWithStatus(status_code)


def is_bad_request():
    return has_status(400)


def is_unauthorized():
    return has_status(403)


def is_not_found():
    return has_status(404)


def is_ok():
    return has_status(200)


class IsHeaderWithValue(BaseMatcher):
    def __init__(self, header, expected_value):
        self.header = header
        self.expected_value = expected_value

    def _matches(self, response):
        return response.headers.get(self.header, None) == self.expected_value

    def describe_to(self, description):
        description.append_text(
            "contain header %s with value %s" % (self.header, self.expected_value))

    def describe_mismatch(self, actual, description):
        description.append_text("had headers %s" % actual.headers.to_list)


def has_header(name, value):
    return IsHeaderWithValue(name, value)


class IsErrorResponse(BaseMatcher):
    def _matches(self, response):
        try:
            data = json.loads(response.data)
            if data.get('status') != 'error':
                return False
            # it should not fail with out a message
            if not data.get('message'):
                return False
            return True
        except ValueError:
            return False

    def describe_to(self, description):
        description.append_text(
            'error response'
        )


def is_error_response():
    return IsErrorResponse()


def d_tz(year, month, day, hour=0, minute=0, seconds=0, tzinfo=None):
    return datetime.datetime(year, month, day, hour, minute, seconds,
                             tzinfo=tzinfo or pytz.UTC)


def d(year, month, day, hour=0, minute=0, second=0):
    return datetime.datetime(year=year, month=month, day=day,
                             hour=hour, minute=minute, second=second)


def fixture_path(name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'features', 'fixtures', name))
