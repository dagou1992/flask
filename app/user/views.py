# coding: utf-8

from app import *
from app.user import user
from db_utils import ModelUtil
from auth_utils import register_login
from flask_login import logout_user, login_required

user_data = [
    {
        'id': 1,
        'name': '张三',
        'age': 23
    },
    {
        'id': 2,
        'name': '李四',
        'age': 24
    }
]

db_name = 'User'
table_name = 'user'


@user.route('/', methods=['POST'])
@login_required
def view_add_user():
    form = request.get_json()
    conditions = {
        "username": form["username"],
    }
    user_message = ModelUtil.query_one(db_name, table_name, conditions)
    if user_message is None:
        ModelUtil.add(db_name, table_name, form)
        return json_response_ok('success')
    else:
        return json_response_error('The username is exist.')


@user.route('/login/', methods=['POST'])
def view_login():
    form = request.get_json()
    conditions = {
        "username": form["username"],
        "password": form["password"],
    }
    user_message = ModelUtil.query_one(db_name, table_name, conditions)
    if user_message is not None:
        user_message.pop("_id")

    if user_message is None:
        return json_response_user_error(), 200
    else:
        register_login(user_message)
        return json_response_ok(user_message)


@user.route('/logout/', methods=['POST'])
@login_required
def view_logout():
    logout_user()
    return json_response_ok('success')


if __name__ == "__main__":
    item = {}
    item["username"] = "jinbangqiang"
    item["role"] = 1
    item['remark'] = "hello world"
    ModelUtil.add(db_name, table_name, item)
