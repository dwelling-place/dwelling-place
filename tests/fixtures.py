# pylint: disable=redefined-outer-name,unused-argument

from datetime import datetime

import pytest

from dwellingplace.app import create_app
from dwellingplace.settings import get_config
from dwellingplace.models import Metric
import red
import red.settings

@pytest.fixture
def app():
    app = create_app(get_config('test'))
    app.testing = True
    return app


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

# FIXME: How to do testing on a composite app?
@pytest.fixture
def redapp():
    return red.create_app(red.settings.get_config('test'))
