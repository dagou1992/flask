# coding: utf-8

from flask_login import LoginManager, UserMixin
from flask_login import login_user

from app import json_response_error

login_manager = LoginManager()


def init_auth(app):
    login_manager.init_app(app)


class User(UserMixin):

    def __init__(self, user):
        self.info = user

    def get_id(self):
        """登录成功后，就会调用get_id()获取到id存入session中"""
        return self.info


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# 在session中记录user已经登录
def register_login(user):
    login_user(User(user))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return json_response_error(401, "用户未登录。"), 401
