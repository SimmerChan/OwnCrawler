import pymongo


class Container(object):
    def __init__(self, db_name, collection_name):
        self.datas = []
        self.connection_mongodb = pymongo.MongoClient()
        self.db = self.connection_mongodb[db_name]
        self.collection = self.db[collection_name]

    def collect_data(self, data):
        if data is None:
            return
        else:
            self.datas.append(data)
            if len(self.datas) >= 10:
                self._output(self.datas)
                self.datas = []

    def _output(self, data):
        self.collection.insert(data)
