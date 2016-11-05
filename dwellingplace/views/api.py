from flask import Blueprint, jsonify

from ..models import Metric


blueprint = Blueprint('api', __name__, url_prefix="/api")


@blueprint.route("/metrics/<PropertyID>/<Date>")
def metric_detail(**kwargs):
    data = Metric.find(**kwargs)

    return jsonify(**data)
