from exts import db
from .base import BaseModel

permissions_menu_table = db.Table('permissions_menu', db.metadata,
                               db.Column("id", db.Integer, primary_key=True, autoincrement=True),
                               db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id')),
                               db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')))


class Permission(BaseModel, db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), comment="权限名称")
    url = db.Column(db.String(200))
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    menu = db.relationship('Menu',
                            secondary=permissions_menu_table,
                            backref=db.backref('permissions', lazy='dynamic'))

    description = db.Column(db.String(100), comment="权限说明")

    def __str__(self):
        return "{title} : {description}".format(title=self.title, description=self.description[:20])
