from datetime import datetime
from random import randint

import pymongo
from bson.timestamp import Timestamp

from utils.logger.Logger import Logger


class Orm:
    def __init__(self, db_name, table_name):
        self.client = None
        self.table = None
        self.db_name = db_name
        self.table_name = table_name

    def __enter__(self):
        uri = f""
        try:
            self.client = pymongo.MongoClient(uri)
            db = self.client[self.db_name]
            self.table = db[self.table_name]

        except Exception as e:
            Logger().Error(str(e), {"db_name": self.db_name, "table_name": self.table_name})
            raise e
        return self

    def __exit__(self, *args):
        self.client.close()

    # sortBy: (key, value)
    def Find(self, obj, limit=1, sortBy=None):
        try:
            if sortBy:
                items = self.table.find(obj, limit=limit).sort(sortBy[0], sortBy[1])
            else:
                items = self.table.find(obj, limit=limit)
            docs = [i for i in items]

        except Exception as e:
            Logger().Error(str(e), {"obj": obj, "limit": limit, "sortBy": sortBy})
            raise e

        return docs

    def Insert(self, objs):
        try:
            for i, obj in enumerate(objs): objs[i]['updated_at'] = Timestamp(datetime.now(), randint(0, 1 << 32 - 1))
            result = self.table.insert_many(objs)

        except Exception as e:
            Logger().Error(str(e), {"objs": objs})
            raise e

        return result.inserted_ids

    def Update(self, query, data):
        try:
            data['updated_at'] = Timestamp(datetime.now(), randint(0, 1 << 32 - 1))
            result = self.table.update_many(query, {"$set": data})

        except Exception as e:
            Logger().Error(str(e), {"query": query, "data": data})
            raise e

        return result.modified_count
