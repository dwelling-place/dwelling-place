# pylint: disable=redefined-outer-name,unused-argument

from datetime import datetime

import pytest

from dwellingplace.app import create_app
from dwellingplace.settings import get_config
from dwellingplace.models import Metric


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    with app.app_context():
        for metric in Metric.objects():
            metric.delete()
    return app.test_client()


@pytest.fixture
def metric(app):
    metric = Metric(
        PropertyID="id1",
        Date=datetime(2016, 11, 5),
        extra=42,
    )
    with app.app_context():
        metric.save()
    return metric
