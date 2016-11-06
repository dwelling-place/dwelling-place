import csv
import io
from collections import OrderedDict
from flask import Blueprint, render_template, request, make_response
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

blueprint = Blueprint('red', __name__)

mongo = PyMongo()


@blueprint.route('/')
def index():
    return render_template('index.html')


api = Api()


def jsonify_doc(doc):
    return {
        k: str(v) if isinstance(v, ObjectId) else v
        for k, v in doc.items()
    }


class Project(Resource):
    def get(self, projid):
        return jsonify_doc(
            mongo.db.projects.find_one_or_404(
                {'_id': ObjectId(projid)}
            )
        )

    def put(self, projid):
        mongo.db.projects.replace_one(
            {'_id': ObjectId(projid)},
            request.form.to_dict()
        )
        return '', 204

    def delete(self, projid):
        mongo.db.projects.delete_one({'_id': ObjectId(projid)})
        return '', 204

api.add_resource(Project, '/projects/<projid>')


class ProjectList(Resource):
    def get(self):
        return [
            jsonify_doc(doc)
            for doc in mongo.db.projects.find()
        ]

    def post(self):
        res = mongo.db.projects.insert_one(request.form.to_dict())
        loc = api.url_for(Project, projid=res.inserted_id)
        return loc, 201, {'Location': loc}

api.add_resource(ProjectList, '/projects')


FIELD_DISPLAY_NAMES = OrderedDict([
    ('name', 'Project'),
    ('address', 'Address'),
    ('start_date', 'Start Date'),
    ('end_date', 'End Date'),
    ('stage', 'Stage'),
    ('completion', 'Completion'),
    ('psh', 'PSH'),
    ('livework', 'Live/Work'),
    ('affordable', 'Aff. Housing'),
    ('commercial', 'Commercial'),
    ('comments', 'Comments/Updates'),
])


def value_display(k, v):
    if not v:
        return v
    elif k == 'completion':
        return float(v) * 100


@blueprint.route('/csv')
def csvdownload():
    buf = io.StringIO()
    dw = csv.DictWriter(buf, FIELD_DISPLAY_NAMES.values())
    dw.writeheader()
    for doc in mongo.db.projects.find():
        dw.writerow({
            FIELD_DISPLAY_NAMES[k]: value_display(k, v)
            for k, v in doc.items() if k in FIELD_DISPLAY_NAMES
        })

    r = make_response(buf.getvalue())
    r.headers['Content-Type'] = 'text/csv'
    r.headers['Content-Disposition'] = 'attachment; filename=RED.csv'

    return r
