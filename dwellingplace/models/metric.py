from collections import OrderedDict

from ..extensions import mongo


class Metric(OrderedDict):

    def __init__(self, PropertyID=None, Date=None, **kwargs):
        super().__init__()
        self['PropertyID'] = PropertyID
        self['Date'] = Date
        self.update(kwargs)

    @staticmethod
    def _documents():
        return mongo.db.metric

    @classmethod
    def objects(cls):
        documents = cls._documents()
        for document in documents.find():
            document.pop('_id')
            yield cls(
                PropertyID=document.pop('PropertyID', None),
                Date=document.pop('Date', None),
                **document,
            )
