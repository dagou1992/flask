# coding: utf-8

from app import *
from app.user import user
from db_utils import ModelUtil
from auth_utils import register_login
from flask_login import logout_user, login_required

db_name = 'User'
table_name = 'user'


def get_user_message(conditions, many=False):
    if many:
        return ModelUtil.query_many(db_name, table_name, conditions)
    else:
        return ModelUtil.query_one(db_name, table_name, conditions)


@user.route('/', methods=['GET'])
@login_required
def view_user_get():
    args = request.args
    conditions = {}
    if args.get('id'):
        conditions["id"] = int(args.get('id'))
    if args.get('username'):
        conditions["username"] = args.get('username')
    if args.get('role'):
        conditions["role"] = int(args.get('role'))
    user_message = get_user_message(conditions, True)
    result = []
    for user in user_message:
        user.pop("_id")
        result.append(user)
    return json_response_ok(result)


@user.route('/', methods=['POST'])
@login_required
def view_user_create():
    form = request.get_json()
    user_message = get_user_message({"username": form["username"]})
    if user_message is None:
        form['mark_list'] = []
        form['review_list'] = []
        ModelUtil.add(db_name, table_name, form)
        return json_response_ok('success')
    else:
        return json_response_error(401, 'The username is exist.'), 200


@user.route('/<int:user_id>', methods=['DELETE'])
@login_required
def view_user_delete(user_id):
    user_message = get_user_message({"id": user_id})
    if user_message is None:
        return json_response_error(401, 'The user is not exist.'), 200
    else :
        ModelUtil.hard_delete(db_name, table_name, {"id": user_id})
        return json_response_ok('success')


@user.route('/<int:user_id>', methods=['PATCH'])
@login_required
def view_user_update(user_id):
    user_message = get_user_message({"id": user_id})
    if user_message is None:
        return json_response_error(401, 'The user is not exist.'), 200
    else:
        form = request.get_json()
        user_message["id"] = user_id
        user_message['username'] = form['username']
        user_message['password'] = form['password']
        user_message['role'] = form['role']
        user_message['remark'] = form['remark'] if 'remark' in form else user_message['remark']
        ModelUtil.update(db_name, table_name, user_message)
        return json_response_ok('success')


@user.route('/login/', methods=['POST'])
def view_login():
    form = request.get_json()
    user_message = get_user_message({
        "username": form["username"],
        "password": form["password"]
    })

    if user_message is None:
        return json_response_error(402, 'The username or password is error.'), 200
    else:
        register_login(user_message)
        user_message.pop("_id")
        return json_response_ok(user_message)


@user.route('/logout/', methods=['POST'])
@login_required
def view_logout():
    logout_user()
    return json_response_ok('success')


if __name__ == "__main__":
    item = {}
    item["username"] = "jinbangqiang"
    item["password"] = "123"
    item["mark_list"] = []
    item["review_list"] = []
    item["role"] = 1
    item["remark"] = 1
    ModelUtil.add(db_name, table_name, item)
