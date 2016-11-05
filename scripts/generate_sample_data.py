#!/usr/bin/env python

import os
from datetime import datetime

from dwellingplace.settings import get_config
from dwellingplace.app import create_app
from dwellingplace import models


def main():
    app = create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    with app.app_context():

        metric = models.Metric('prop1', datetime(2016, 11, 5))
        metric.save()

        metric = models.Metric('prop2', datetime(2016, 11, 5), extra="foobar")
        metric.save()


if __name__ == '__main__':
    main()
