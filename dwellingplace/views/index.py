from flask import Blueprint, render_template, send_file

from ..models import Metric, save_json


blueprint = Blueprint('index', __name__)


@blueprint.route("/")
def get():
    formats = [
        # ('xlsx', "Excel"),
        # ('csv', "CSV"),
        ('json', "JSON"),
    ]
    return render_template("index.html", formats=formats)


@blueprint.route("/downlaod", methods=['POST'])
def download():
    data = Metric.objects()
    path = save_json(data, "/tmp/metrics.json")

    return send_file(path, as_attachment=True)
