# @Time     : 2019/4/2 16:57
# @Author   : sonny.zhang
# @FileName : decorators.py
# @github   : @sonny-zhang
from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    """<装饰器>校验权限"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('权限不足.')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
