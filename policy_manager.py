import json
import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://bogdan:Cemaifaci5%3F@mongo.jpa8i.mongodb.net/test")

database_politics = myclient["Politici"]
collection_politics = database_politics["policies"]
agents = database_politics["agents"]


def insert_policy(data):
    dict = {'_id': int(data['_id']), 'policy_name': data['policy_name'], 'rules': data['rules'],
            'time_start': datetime.strptime(data['time_start'], '%d-%m-%y %H:%M:%S'),
            'time_stop': datetime.strptime(data['time_stop'], '%d-%m-%y %H:%M:%S'), 'order': data['order']}

    x = collection_politics.insert_one(dict)


def update_policy(data):
    keys = list(data.keys())
    rule_id = 0
    if len(keys) == 3:
        rule_id = keys[2]
        camp_pt_update = keys[1]
        new_value = data[camp_pt_update]
    elif len(keys) == 2:
        camp_pt_update = keys[1]
        new_value = data[camp_pt_update]
    else:
        return "eroare"

    dict_ext = ['_id', 'policy_name', 'time_start', 'time_stop', 'order']
    dict_int = ['rule_id', 'rule_name', 'description', 'domain', 'destination', 'source', 'action', 'direction']

    if camp_pt_update in dict_ext:
        collection_politics.update_one({'_id': data["_id"]}, {'$set': {camp_pt_update: new_value}})

    if camp_pt_update in dict_int:
        collection_politics.update_one({'_id': data["_id"], "rules.rule_id": data["rule_id"]},
                                       {'$set': {f"rules.$.{camp_pt_update}": new_value}})

    return collection_politics.find_one({'_id': data["_id"]})


if __name__ == "__main__":
    pass
