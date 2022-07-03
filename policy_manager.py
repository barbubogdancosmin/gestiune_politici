import json
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://bogdan:Cemaifaci5%3F@mongo.jpa8i.mongodb.net/test")

database_politics = myclient["Politici"]
collection_politics = database_politics["database_for_politics"]


def insert_policy(data):
    dict = {'_id': data['_id'], 'policy_name': data['policy_name'], 'rules': data['rules'],
            'time_start': data['time_start'], 'time_stop': data['time_stop'], 'order': data['order']}

    x = collection_politics.insert_one(dict)


def delete_policy():
    print("Ati ales sa stergeti o politica.\n")
    for x in collection_politics.find():
        json_obj = json.dumps(x, indent=4)
        print(json_obj)
    id = input("Va rugam introduceti id-ul politicii pe care doriti sa o stergeti: ")
    collection_politics.delete_one({'_id': id})
    print('S-a sters cu succes!')


def update_policy(data):
    keys = list(data.keys())
    camp_pt_update = keys[1]
    new_value = data[camp_pt_update]

    dict_ext = ['_id', 'policy_name', 'time_start', 'time_stop', 'order']
    dict_int = ['rule_id', 'rule_name', 'description', 'domain', 'destination', 'source', 'action', 'direction']

    if camp_pt_update in dict_ext:
        collection_politics.update_one({'_id': data["_id"]}, {'$set': {camp_pt_update: new_value}})

    if camp_pt_update in dict_int:
        collection_politics.update_one({'_id': data["_id"]}, {'$set': {f"rules.{camp_pt_update}": new_value}})

    return collection_politics.find_one({'_id': data["_id"]})


if __name__ == "__main__":
    pass
