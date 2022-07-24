from exts import db
from .base import BaseModel

role_permission_table = db.Table('role_permission', db.metadata,
                               db.Column("id", db.Integer, primary_key=True, autoincrement=True),
                               db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                               db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')))


class Role(BaseModel, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), comment="角色名称")
    description = db.Column(db.String(100), comment="角色说明")

    permission = db.relationship('Permission',
                            secondary=role_permission_table,
                            backref=db.backref('roles', lazy='dynamic'))

    # permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    # permission = db.relationship("Permission", backref='permission')
    def __str__(self):
        return "{title} : {description}".format(title=self.title, description=str(self.description)[:20])
