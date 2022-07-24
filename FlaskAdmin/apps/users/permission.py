# -*- coding: UTF-8 -*-
import io
import sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

from flask import request
from . import user_app
from apps.models.permissions import Permission
from pkg.response.response import Response
from exts import db


@user_app.route("/permission/add", methods=['POST'])
def permission_add():
    """
    权限新增
    :return:
    """
    title = request.form.get('title')
    url = request.form.get('url')
    if title and len(Permission.query.filter(Permission.url == url, Permission.is_deleted == 0).all()) == 0:
        permission = Permission()
        permission.title = title
        permission.url = url
        db.session.add(permission)
        db.session.commit()
        return Response("200", 200, "创建角色成功")
    return Response("300", 300, "创建角色失败")


@user_app.route("/permission/delete", methods=['POST'])
def permission_delete():
    """
    删除权限
    :return:
    """
    permission_id = request.form.get('permissionId')
    permissions = Permission.query.filter(Permission.id == permission_id).all()
    for permission in permissions:
        permission.is_deleted = 1
        db.session.add(permission)
        db.session.commit()
    return Response("200", 200, "删除权限成功")
