import unittest
import urllib
import datetime
from hamcrest import *
from mock import patch, Mock
import pytz
from backdrop.core.timeseries import WEEK
from backdrop.read import api
from backdrop.read.query import Query
from tests.support.bucket import stub_bucket_retrieve_by_name
from tests.support.test_helpers import has_status

from warnings import warn


class NoneData(object):
    def data(self):
        return None


warn("This test is deprecated in favour of "
     "tests.read.test_read_api_service_data_endpoint")


class QueryingApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    @stub_bucket_retrieve_by_name("foo", raw_queries_allowed=True)
    @patch('backdrop.core.bucket.Bucket.query')
    def test_filter_by_query_is_executed(self, mock_query):
        mock_query.return_value = NoneData()
        self.app.get('/foo?filter_by=zombies:yes')
        mock_query.assert_called_with(
            Query.create(filter_by=[[u'zombies', u'yes']]))

    @stub_bucket_retrieve_by_name("foo")
    @patch('backdrop.core.bucket.Bucket.query')
    def test_group_by_query_is_executed(self, mock_query):
        mock_query.return_value = NoneData()
        self.app.get('/foo?group_by=zombies')
        mock_query.assert_called_with(
            Query.create(group_by=u'zombies'))

    @stub_bucket_retrieve_by_name("foo", raw_queries_allowed=True)
    @patch('backdrop.core.bucket.Bucket.query')
    def test_query_with_start_and_end_is_executed(self, mock_query):
        mock_query.return_value = NoneData()
        expected_start_at = datetime.datetime(2012, 12, 5, 8, 12, 43,
                                              tzinfo=pytz.UTC)
        expected_end_at = datetime.datetime(2012, 12, 12, 8, 12, 43,
                                            tzinfo=pytz.UTC)
        self.app.get(
            '/foo?start_at=' + urllib.quote("2012-12-05T08:12:43+00:00") +
            '&end_at=' + urllib.quote("2012-12-12T08:12:43+00:00")
        )
        mock_query.assert_called_with(
            Query.create(start_at=expected_start_at, end_at=expected_end_at))

    @stub_bucket_retrieve_by_name("foo", raw_queries_allowed=True)
    @patch('backdrop.core.bucket.Bucket.query')
    def test_sort_query_is_executed(self, mock_query):
        mock_query.return_value = NoneData()
        self.app.get(
            '/foo?sort_by=value:ascending'
        )
        mock_query.assert_called_with(
            Query.create(sort_by=["value", "ascending"]))

        self.app.get(
            '/foo?sort_by=value:descending'
        )
        mock_query.assert_called_with(
            Query.create(sort_by=["value", "descending"]))

    @stub_bucket_retrieve_by_name("bucket", queryable=False)
    def test_returns_404_when_bucket_is_not_queryable(self):
        response = self.app.get('/bucket')
        assert_that(response, has_status(404))


class PreflightChecksApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    @stub_bucket_retrieve_by_name("bucket")
    def test_cors_preflight_requests_have_empty_body(self):
        response = self.app.open('/bucket', method='OPTIONS')
        assert_that(response.status_code, is_(200))
        assert_that(response.data, is_(""))

    @stub_bucket_retrieve_by_name("bucket")
    def test_cors_preflight_are_allowed_from_all_origins(self):
        response = self.app.open('/bucket', method='OPTIONS')
        assert_that(response.headers['Access-Control-Allow-Origin'], is_('*'))

    @stub_bucket_retrieve_by_name("bucket")
    def test_cors_preflight_result_cache(self):
        response = self.app.open('/bucket', method='OPTIONS')
        assert_that(response.headers['Access-Control-Max-Age'],
                    is_('86400'))

    @stub_bucket_retrieve_by_name("bucket")
    def test_cors_requests_can_cache_control(self):
        response = self.app.open('/bucket', method='OPTIONS')
        assert_that(response.headers['Access-Control-Allow-Headers'],
                    is_('cache-control'))
