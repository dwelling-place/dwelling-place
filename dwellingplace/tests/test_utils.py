# pylint: disable=unused-argument,unused-variable,expression-not-assigned

import os
from datetime import datetime

import pytest
from expecter import expect
import xlrd

from dwellingplace.models._utils import parse_xlsx_into_dicts, get_value

DATA = os.path.join(os.path.dirname(__file__), "data")


def test_load():
    xl = xlrd.open_workbook(os.path.join(DATA, 'sample.xlsx'))
    output = list(parse_xlsx_into_dicts(xl))
    assert output[0]['Curb Appeal'] == 4.3
    assert output[0]['Date'] == datetime(2016, 9, 1)


def describe_get_value():

    @pytest.fixture
    def datum():
        return dict(
            _int=1,
            _float=2.3,
            _float_percent=0.5,
            _str="Hello, world!",
            _bool=True,
            _date=datetime(2016, 11, 5),

        )

    def when_int(datum):
        expect(get_value(datum, '_int')) == (1, None)

    def when_float(datum):
        expect(get_value(datum, '_float')) == (2.3, None)

    def when_float_as_a_percentage(datum):
        expect(get_value(datum, '_float_percent')) == \
            (0.5, {'num_format': "0.00%"})

    def when_bool(datum):
        expect(get_value(datum, '_bool')) == (True, None)

    def when_date(datum):
        expect(get_value(datum, '_date')) == \
            (datetime(2016, 11, 5), {'num_format': "mmm yyyy"})
