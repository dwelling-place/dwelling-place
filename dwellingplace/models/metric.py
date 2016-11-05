from collections import OrderedDict

from ..extensions import mongo


class Metric(OrderedDict):

    def __init__(self, PropertyID=None, Date=None, **kwargs):
        super().__init__()
        self['PropertyID'] = PropertyID
        self['Date'] = Date
        self.update(kwargs)

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
    def objects(cls):
        documents = cls._documents()
        for document in documents.find():
            document.pop('_id')
            yield cls(
                PropertyID=document.pop('PropertyID', None),
                Date=document.pop('Date', None),
                **document,
            )

    def save(self):
        documents = self._documents()
        documents.replace_one(self.key, self, upsert=True)
