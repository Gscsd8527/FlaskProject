from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from .base import BaseModel

user_role_table = db.Table('user_role', db.Model.metadata,
                             db.Column("id", db.Integer, primary_key=True, autoincrement=True)
                           , db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                           , db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

user_organization_table = db.Table('user_organization', db.Model.metadata,
                             db.Column("id", db.Integer, primary_key=True, autoincrement=True)
                           , db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                           , db.Column('organization_id', db.Integer, db.ForeignKey('departments.id')))


class User(BaseModel, db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True)

    login_time = db.Column(db.DateTime, index=True, default=datetime.now(), comment='登录时间')
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    roles = db.relationship('Role',
                            secondary=user_role_table,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy="dynamic")

    # department_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    department = db.relationship('Organization',
                                 secondary=user_organization_table,
                                 backref=db.backref('users', lazy='dynamic'),
                                 lazy="dynamic")

    @property
    def password(self):
        return AttributeError(u'该属性不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

    def to_json(self):
        json = {
            'userId': self.id,
            'username': self.username,
            'name': self.name,
            'sex': self.sex,
            'age': self.age,
            'phone': self.phone,
            'email': self.email,
            'roles': self.get_roles(),
            'department': self.get_department(),
            'permissions': self.get_permissions()
        }
        return json

    def get_roles(self):
        """
        获取当前用户的角色列表
        :return:
        """
        roles = list()
        roles.extend([{'roleId': _.id, "title": _.title} for _ in self.roles])
        return roles

    def get_department(self):
        """
        获取当前用户下的部门
        :return:
        """
        departments = list()
        departments.extend([{'departmentId': _.id, "title": _.name} for _ in self.department])
        return departments

    def get_permissions(self):
        """
        获取当前用户下的权限列表
        :return:
        """
        permissionList = list()
        for role in self.roles:
            permissions = role.permission
            for permission in permissions:
                permissionList.append({"permissionId": permission.id, "title": permission.title, 'url': permission.url})
        return permissionList
