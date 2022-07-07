from flask import Blueprint, request
from __init__ import create_app, db
import os
import policy_manager
from auth_middleware import token_required
from bson import json_util
from flask import json
from werkzeug.exceptions import HTTPException
from bson import ObjectId

main = Blueprint('main', __name__)


@main.route('/show_agents', methods=['GET'])
@token_required
def show_agents(current_user):
    lista = []
    for x in policy_manager.agents.find():
        lista.append(x)
    agents = json_util.dumps(lista, indent=4)
    return agents


@main.route('/show_policies', methods=['GET'])
@token_required
def show_policies(current_user):
    lista = []
    for x in policy_manager.collection_politics.find():
        lista.append(x)
    policies = json_util.dumps(lista, indent=4)
    return policies


@main.route('/show_policy/<id>', methods=['GET'])
@token_required
def show_policy(current_user, id):
    for x in policy_manager.collection_politics.find():
        if x['_id'] == int(id):
            return json_util.dumps(x, indent=4)


@main.route('/insert', methods=['POST'])
@token_required
def insert(current_user):
    data = request.json
    for elem in data['rules']:
        elem['rule_id'] = int(elem['rule_id'])
    policy_manager.insert_policy(data)
    return data


@main.route('/update', methods=['POST'])
@token_required
def update(current_user):
    data = request.json
    return policy_manager.update_policy(data)


@main.route('/delete/<id>', methods=['DELETE'])
@token_required
def delete(curent_user, id):
    for x in policy_manager.collection_politics.find():
        if x['_id'] == int(id):
            policy_manager.collection_politics.delete_one({'_id': x['_id']})
            return '204'


app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True, port=int(os.environ.get('PORT', 5050)), host='0.0.0.0')
