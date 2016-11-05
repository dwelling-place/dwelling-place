import os

import xlrd

from dwellingplace.models._utils import parse_xlsx_into_dicts, merge_metrics_from_dicts


def test_load():
    xl = xlrd.open_workbook(os.path.join(os.path.dirname(__file__), 'data/sample.xlsx'))
    parse_xlsx_into_dicts(xl)
