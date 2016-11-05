# pylint: disable=no-member

import json
import logging

import openpyxl


log = logging.getLogger(__name__)


def save_json(data, path):
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return path


def save_xlsx(data, path):
    log.debug("Creating %s", path)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Add header row
    header = _get_header(data)
    log.debug("Header: %s", header)
    worksheet.append(header)

    # Enable filtering on every column
    worksheet.auto_filter.ref = "A1:ZZ9999"
    for index in range(len(header)):
        worksheet.auto_filter.add_filter_column(index, [])

    # Add data rows
    for datum in data:
        row = [datum.get(key, '') for key in header]
        log.debug("Row: %s", row)
        worksheet.append(row)

    workbook.save(path)

    return path


def _get_header(data):
    """Collect column names from every data set."""
    header = set()

    for datum in data:
        header.update(datum.keys())

    return list(header)
