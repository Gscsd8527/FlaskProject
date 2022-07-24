from flask import request
from . import user_app
from apps.models.user import User
from apps.models.role import Role
from pkg.response.response import Response
from exts import db
import json


@user_app.route("/")
def hello():
    data = [{'a': 'b'}, {'b': 'c'}, {'c': 'd'}]
    return Response('400', code=200, data=data)


@user_app.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        return Response("200", 200, "")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if all([username, password]):
            user_list = User.query.filter(User.username == username).all()
            for user in user_list:
                if user.check_password(password):
                    print(user)
                    return Response("200", 200, user.to_json())
            return Response("300", 200, "用户名密码错误")
        else:
            return Response("300", 200, "用户名密码漏填")


@user_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return Response("200", 200, "")
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        if all([username, password1, password2]):
            if password1 != password2:
                return Response("300", 300, "")

            user = User.query.filter(User.username == username).first()
            if user:
                return Response("300", 300, "")
            else:
                user = User()
                user.username = username
                user.password = password1
                user.email = email
                db.session.add(user)
                db.session.commit()
                # 生成一个token
                return Response("200", 200, "")

        else:
            return Response("200", 200, "")


@user_app.route('/authRole', methods=['POST'])
def grant_user_role():
    data_json = json.loads(request.get_data().decode('utf-8'))
    userId = data_json.get("userId")
    roleIds = data_json.get("roleIds")
    user = User.query.get(userId)
    if not roleIds:
        user.roles = []
    else:
        for id in roleIds:
            user.roles.append(Role.query.get(id))

    db.session.add(user)
    db.session.commit()
    return Response("200", 200, "操作成功")

