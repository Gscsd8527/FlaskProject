from exts import db
from .base import BaseModel


class Organization(BaseModel, db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), comment="名称")
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship("Organization", remote_side=[department_id])
    description = db.Column(db.String(100), comment="组织机构说明")

    def __str__(self):
        return "{name} : {description}".format(name=self.name, description=str(self.description)[:20])
