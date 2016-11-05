import xlrd

from flask import Blueprint, request, render_template, send_file, Response
from flask_login import login_required

from ..models import Metric, save_xlsx, save_json
from ..models._utils import parse_xlsx_into_dicts, merge_metrics_from_dicts


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    formats = [
        ('xlsx', "Excel"),
        # ('csv', "CSV"),
        ('json', "JSON"),
    ]
    return render_template("index.html", formats=formats)


@blueprint.route("/download", methods=['POST'])
def download():
    ext = request.form['format']

    data = list(Metric.objects())
    if ext == 'xlsx':
        path = save_xlsx(data, "/tmp/metrics.xlsx")
    elif ext == 'json':
        path = save_json(data, "/tmp/metrics.json")

    return send_file(path, as_attachment=True)


@blueprint.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    xl = xlrd.open_workbook(file_contents=file.stream.read())
    try:
        merge_metrics_from_dicts(parse_xlsx_into_dicts(xl))
    except TypeError as err:
        return err.message
    return 'Upload success.'


@blueprint.route("/protected/", methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)
