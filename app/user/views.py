# coding: utf-8

from app import *
from app.user import user
from db_utils import ModelUtil

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


@user.route('/<int:id>', methods=['GET'])
def get(id):
    for user in user_data:
        if user['id'] == id:
            return json_response_ok(user)


@user.route('/', methods=['GET'])
def users():
    return json_response_ok(user_data)


if __name__ == "__main__":
    item = {}
    item["username"] = "jinbangqiang"
    item["password"] = "123"
    item["role"] = 1
    item['remark'] = "hello world"
    ModelUtil.add(db_name, table_name, item)
