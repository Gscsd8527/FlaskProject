from flask import request
from . import user_app
from apps.models.role import Role
from apps.models.permissions import Permission
from pkg.response.response import Response
from exts import db
import json


@user_app.route("/role/add", methods=['POST'])
def role_add():
    """
    角色新增
    :return:
    """
    title = request.form.get('title')
    if title and len(Role.query.filter(Role.title == title).all()) == 0:
        role = Role()
        role.title = title
        db.session.add(role)
        db.session.commit()
        return Response("200", 200, "创建角色成功")
    return Response("300", 300, "")


@user_app.route("/role/delete", methods=['POST'])
def role_delete():
    """
    角色删除
    :return:
    """
    roleId = request.form.get('roleId')
    if roleId and Role.query.filter(Role.id == roleId):
        role = Role.query.get(roleId)
        db.session.delete(role)
        db.session.commit()
        return Response("200", 200, "删除角色成功")
    return Response("300", 300, "")


@user_app.route("/role/permission/add", methods=['POST'])
def role_permission_add():
    """
    为角色增加权限
    :return:
    """
    data_json = json.loads(request.get_data().decode('utf-8'))
    roleId = data_json.get("roleId")
    permissionIds = data_json.get("permissionId")
    role = Role.query.get(roleId)
    if not permissionIds:
        role.permission = []
    else:
        role.permission = [Permission.query.get(permissionId) for permissionId in permissionIds]
    db.session.add(role)
    db.session.commit()
    return Response("200", 200, "为角色增加权限 - 操作成功")


@user_app.route("/role/permission/delete", methods=['POST'])
def role_permission_delete():
    """
    为角色减少权限
    :return:
    """
    data_json = json.loads(request.get_data().decode('utf-8'))
    roleId = data_json.get("roleId")
    permissionIds = data_json.get("permissionId")
    role = Role.query.get(roleId)
    if not permissionIds:
        role.permission = []
    else:
        role.permission = [Permission.query.get(permissionId) for permissionId in permissionIds]
    db.session.delete(role)
    db.session.commit()
    return Response("200", 200, "为角色增加权限 - 操作成功")
