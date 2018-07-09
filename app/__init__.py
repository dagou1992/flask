
from flask import jsonify
from flask import request


def json_response_error(code=500, error='服务器出错了'):
    data = {
        'code': code,
        'error': error,
        'data': '',
    }
    r = jsonify(data)
    return r


def json_response_ok(data, error='', code=200):
    data = {
        'code': code,
        'error': error,
        'data': data,
    }
    r = jsonify(data)
    return r


def json_response_user_error(code=401, error='用户名或密码错误'):
    data = {
        'code': code,
        'error': error,
        'data': '',
    }
    r = jsonify(data)
    return r
