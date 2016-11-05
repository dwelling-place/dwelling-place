import os
from datetime import datetime

import xlrd

from dwellingplace.models._utils import parse_xlsx_into_dicts, merge_metrics_from_dicts


def test_load():
    xl = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), 'data/sample.xlsx'))
    output = list(parse_xlsx_into_dicts(xl))
    assert output[0]['Curb Appeal'] == 4.3
    assert output[0]['Date'] == datetime(2016, 9, 1)
