import sys
from datetime import datetime

import xlrd
from xlrd.biffh import XLRDError

from flask import Blueprint, request, render_template, send_file
from flask import flash, redirect, url_for

from ..models import Metric, Structure, save_xlsx, save_json
from ..models._utils import parse_xlsx_into_dicts, merge_metrics_from_dicts, update_structure
from ._utils import get_filename


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    formats = [
        ('xlsx', "Excel"),
        # ('csv', "CSV"),
        ('json', "JSON"),
    ]
    structure = Structure.load()
    months = sorted(Metric.months(), reverse=True)
    return render_template("index.html",
                           formats=formats,
                           structure=structure,
                           months=months)


@blueprint.route("/download", methods=['POST'])
def download():
    ext = request.form['format']
    sheets = request.form.getlist('sheets')
    months = [
        datetime.strptime(m, '%b %Y')
        for m in request.form.getlist('months')
    ]

    data = list(Metric.objects(dates=months))
    filename = get_filename("metrics", ext)
    if ext == 'xlsx':
        path = save_xlsx(data, sheets, filename, prefill=True)
    elif ext == 'json':
        path = save_json(data, filename)

    return send_file(path, as_attachment=True)


@blueprint.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    try:
        xl = xlrd.open_workbook(file_contents=file.stream.read())
    except XLRDError:
        flash('Upload Failed: The file was probably not an Excel workbook.',
              "message-upload-fail")
    else:
        try:
            update_structure(xl, Structure.load())
            merge_metrics_from_dicts(parse_xlsx_into_dicts(xl))
        except TypeError as err:
            flash('Upload Failed: ' + err.message, "message-upload-fail")
        except KeyError:
            flash('Upload Failed: You may have uploaded the wrong file or ' +
                  'the format is corrupt.', "message-upload-fail")
        except:  # pylint: disable=bare-except
            flash('Upload Failed: The reported error was: {} {}'.
                  format(sys.exc_info()[0], sys.exc_info()[1]),
                  "message-upload-fail")
        else:
            flash('Upload successful.', "message-upload-success")
    return redirect(url_for('index.get'))
