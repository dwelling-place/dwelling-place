# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison,redefined-outer-name

from datetime import datetime

import pytest
from expecter import expect

from dwellingplace.models import Metric


@pytest.fixture
def date():
    return datetime(2016, 11, 5)


def describe_metrics():

    def describe_init():

        def it_requires_property_id(date):
            with expect.raises(ValueError, "Invalid ID: None"):
                Metric(Date=date)

        def it_requires_a_date(date):
            with expect.raises(ValueError, "Invalid date: None"):
                Metric(PropertyID='foobar')

        def it_requires_a_valid_date(date):
            with expect.raises(ValueError, "Invalid date: '2016/10'"):
                Metric(PropertyID='foobar', Date="2016/10")
