from collections import OrderedDict
from datetime import datetime

import pymongo

from ..extensions import mongo


class Metric(OrderedDict):

    def __init__(self, PropertyID=None, Date=None, **kwargs):
        super().__init__()
        if not PropertyID:
            raise ValueError("Invalid ID: {!r}".format(PropertyID))
        self['PropertyID'] = PropertyID
        if not isinstance(Date, datetime):
            raise ValueError("Invalid date: {!r}".format(Date))
        self['Date'] = Date
        self.update(kwargs)

    @classmethod
    def create_indexes(cls):
        cls._documents().create_index([('Date', pymongo.ASCENDING),
                                       ('PropertyID', pymongo.ASCENDING)])

    @property
    def key(self):
        return dict(PropertyID=self['PropertyID'], Date=self['Date'])

    @staticmethod
    def _documents():
        return mongo.db.metric

    @classmethod
    def find(cls, **kwargs):
        documents = cls._documents()
        document = documents.find_one(kwargs)
        if document:
            document.pop('_id')
            return cls(
                PropertyID=document.pop('PropertyID', None),
                Date=document.pop('Date', None),
                **document,
            )
        else:
            return cls(
                PropertyID=kwargs.get('PropertyID'),
                Date=kwargs.get('Date'),
            )

    @classmethod
    def objects(cls, dates=None):
        documents = cls._documents()
        query = {}
        if dates:
            query['Date'] = {'$in': dates}
        sort = [
            ('Date', pymongo.ASCENDING),
            ('PropertyID', pymongo.ASCENDING),
        ]
        for document in documents.find(query).sort(sort):
            document.pop('_id')
            yield cls(
                PropertyID=document.pop('PropertyID', None),
                Date=document.pop('Date', None),
                **document,
            )

    def save(self):
        documents = self._documents()
        documents.replace_one(self.key, self, upsert=True)

    def delete(self):
        documents = self._documents()
        documents.delete_one(self.key)

    @classmethod
    def months(cls):
        documents = cls._documents()
        return documents.distinct('Date')
