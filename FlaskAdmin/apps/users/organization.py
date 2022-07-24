
from flask import request
from . import user_app
from apps.models.organizations import Organization
from pkg.response.response import Response
from exts import db


@user_app.route("/organization/add", methods=['POST'])
def organization_add():
    """
    机构的新增
    :return:
    """
    title = request.form.get('title')
    organizationId = request.form.get('organizationId')
    if organizationId is None:
        if title and len(Organization.query.filter(Organization.name == title).all()) == 0:
            organization = Organization()
            organization.name = title
            db.session.add(organization)
            db.session.commit()
            return Response("200", 200, "创建机构成功")
    else:
        if title and len(Organization.query.filter(Organization.name == title).all()) == 0:
            organization = Organization()
            organization.name = title
            organization.department_id = organizationId
            db.session.add(organization)
            db.session.commit()
            return Response("200", 200, "创建机构成功")

    return Response("300", 300, "")


@user_app.route("/organization/delete", methods=['POST'])
def organization_delete():
    """
    机构的删除
    :return:
    """
    organization_id = request.form.get('organizationId')
    organizations = Organization.query.filter(Organization.id == organization_id).all()
    for organization in organizations:
        organization.is_deleted = 1
        db.session.add(organization)
        db.session.commit()
    return Response("200", 200, "删除机构成功")
