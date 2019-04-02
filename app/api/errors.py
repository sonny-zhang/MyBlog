# @Time     : 2019/4/2 14:51
# @Author   : sonny.zhang
# @FileName : errors.py
# @github   : @sonny-zhang
from flask import jsonify
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': '错误请求', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': '没有授权', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': '被禁用', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
