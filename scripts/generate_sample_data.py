#!/usr/bin/env python

import os

from dwellingplace.settings import get_config
from dwellingplace.app import create_app
from dwellingplace import models


def main():
    create_app(get_config(os.getenv('FLASK_ENV') or 'dev'))

    metric = models.Meric()


if __name__ == '__main__':
    main()
