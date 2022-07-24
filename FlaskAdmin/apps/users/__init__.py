from flask import Blueprint
user_app = Blueprint('user_app', __name__)

# 在__init__.py文件被执行的时候，把视图加载进来，让蓝图与应用程序知道有视图的存在
from .user import hello, login, register
from .role import role_add, role_delete, role_permission_add, role_permission_delete
from .permission import permission_add, permission_delete
from .organization import organization_add
