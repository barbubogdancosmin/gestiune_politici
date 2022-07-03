from flask import Blueprint, request
from __init__ import create_app, db
import os
import policy_manager
from auth_middleware import token_required
from bson import json_util
from flask import json
from werkzeug.exceptions import HTTPException

main = Blueprint('main', __name__)


@main.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


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
    if policy_manager.collection_politics.find_one({'_id': id}):
        return policy_manager.collection_politics.find_one({'_id': id})
    else:
        return 'Id not in database'


@main.route('/insert', methods=['POST'])
@token_required
def insert(current_user):
    data = request.json
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
    policy_manager.collection_politics.delete_one({'_id': id})
    return '204'


app = create_app()

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run(debug=True, port=int(os.environ.get('PORT', 5050)), host='0.0.0.0')
