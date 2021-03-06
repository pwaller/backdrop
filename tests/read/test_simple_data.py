import unittest
from hamcrest import *
from backdrop.read.response import SimpleData
from tests.support.test_helpers import d_tz, d


class TestSimpleData(unittest.TestCase):
    def test_adding_documents_converts_timestamps_to_utc(self):
        stub_document = {
            "_timestamp": d(2014, 1, 1)
        }
        data = SimpleData([stub_document])
        assert_that(data.data(), has_length(1))
        assert_that(data.data()[0], has_entry("_timestamp",
                                              d_tz(2014, 1, 1)))

    def test_returned_data_should_be_immutable(self):
        stub_doc = {
            "_timestamp": d(2014, 1, 1)
        }
        data = SimpleData([stub_doc])
        another_data = data.data()
        try:
            another_data.append({"even_more_nonsense": True})
            assert_that(False, "expected an exception")
        except AttributeError as e:
            assert_that(str(e), "'tuple' object has no attribute append")
