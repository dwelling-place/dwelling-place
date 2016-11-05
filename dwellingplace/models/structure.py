from collections import OrderedDict

from ..extensions import mongo


class Structure(OrderedDict):
    """
    serialize into Mongo as two fields so that we keep track of the order of sheets (mongo forgets dict order)
    {
    sheet_order: ["Foo", "Bar", "Baz"],
    sheet_columns: {
            Foo: ["PropertyID", "Date", "x", "y", z"],
            Bar: ["PropertyID", "Date", "asdf", "blah", "blaise"],
            Baz: ["PropertyID", "Date", "tbd", "doa", "roi"],
        }
    }
    """

    @staticmethod
    def _documents():
        return mongo.db.structure

    @classmethod
    def load(cls):
        doc = cls._documents().find_one()
        if not doc:
            return cls()

        structure = cls()
        for sheet in doc['sheet_order']:
            structure[sheet] = doc['sheet_columns'][sheet]
        return structure

    def save(self):
        doc = {
            'sheet_order': list(self.keys()),
            'sheet_columns': self,
        }
        self._documents().replace_one({'_id': 1}, doc, upsert=True)
