# @Time     : 2019/3/22 11:19
# @Author   : sonny.zhang
# @FileName : decorators.py
# @github   : @sonny-zhang
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    """[带参数的装饰器]检查常规权限
    :param permission: 权限位
    :return: 函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """检查admin权限"""
    return permission_required(Permission.ADMIN)(f)
