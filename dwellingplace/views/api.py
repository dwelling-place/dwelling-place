from datetime import datetime

from flask import Blueprint, jsonify

from ..models import Metric


blueprint = Blueprint('api', __name__, url_prefix="/api")


@blueprint.route("/metrics/")
def metrics():
    data = list(Metric.objects())

    return jsonify(data)


@blueprint.route("/metrics/<key>/<int:year>/<int:month>/<int:day>")
def metrics_detail(key, year, month, day):
    datum = Metric.find(
        PropertyID=key,
        Date=datetime(year, month, day),
    )

    return jsonify(**datum)
