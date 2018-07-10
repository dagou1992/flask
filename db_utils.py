from config import client


def timestamp():
    import time
    return int(time.time())


def next_id(db_name, name):
    mongua = client[db_name]
    item = ModelUtil.query_one(db_name, "data_id", {'name': name}, False)
    '''
    Not delete it until initialize script is done. Please.
    '''
    if item is None:
        mongua['data_id'].insert({'name': name, 'seq': 0})
        item = ModelUtil.query_one(db_name, "data_id", {'name': name}, False)
    new_id = item["seq"] + 1
    item["seq"] += 1
    ModelUtil.update(db_name, "data_id", item)
    return new_id


class ModelUtil:

    @classmethod
    def add(cls, db_name, table_name, item):
        mongua = client[db_name]
        table = mongua[table_name]
        item["id"] = next_id(db_name, table_name)
        item["deleted"] = False
        ts = timestamp()
        item["created_time"] = ts
        item["updated_time"] = ts

        table.insert_one(item)
        return item

    @classmethod
    def delete(cls, db_name, table_name, conditions):
        item = cls.query_one(db_name, table_name, conditions)
        if item is not None:
            item["deleted"] = True
            item["updated_time"] = timestamp()
            cls.update(db_name, table_name, item)
            return item

    @classmethod
    def query_one(cls, db_name, table_name, conditions, exists=True):
        mongua = client[db_name]
        table = mongua[table_name]
        if exists:
            if conditions is not None:
                conditions['deleted'] = False
            else:
                conditions = {'deleted': False}
        item = table.find_one(conditions)
        return item

    @classmethod
    def exists(cls, db_name, table_name, conditions):
        mongua = client[db_name]
        table = mongua[table_name]
        item = table.find_one(conditions)
        return item is not None and item["deleted"] == False

    @classmethod
    def update(cls, db_name, table_name, item):
        mongua = client[db_name]
        table = mongua[table_name]
        item["updated_time"] = timestamp()
        table.save(item)
        return item

    @classmethod
    def query_many(cls, db_name, table_name, conditions=None, projection=None, exists=True):
        mongua = client[db_name]
        table = mongua[table_name]
        if exists:
            if conditions is not None:
                conditions['deleted'] = False
            else:
                conditions = {'deleted': False}
        item = table.find(conditions, projection)
        return item

    @classmethod
    def hard_delete(cls, db_name, table_name, conditions):
        mongua = client[db_name]
        table = mongua[table_name]
        item = cls.query_one(db_name, table_name, conditions, exists=False)
        if item is not None:
            table.delete_one(item)

    @classmethod
    def delete_many(cls, db_name, table_name, id_list):
        mongua = client[db_name]
        table = mongua[table_name]
        table.update_many({'id': {'$in': id_list}}, {'$set': {'deleted': True}})
