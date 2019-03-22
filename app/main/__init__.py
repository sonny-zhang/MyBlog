# @Time     : 2019/3/6 21:31
# @Author   : sonny-zhang
# @FileName : __init__.py
# @Blog     : http://www.cnblogs.com/1fengchen1/

from flask import Blueprint

#: 创建蓝图
main = Blueprint('main', __name__)

#: 初始化其他模块。必须放在创建蓝图的后面，否则导入包会包找不到main蓝图实例。(urls里导入了views，所以不用加载了)
from . import urls, errors
from app.models import Permission


@main.app_context_processor
def inject_permissions():
    """将Permission添加到上下文处理器"""
    return dict(Permission=Permission)
