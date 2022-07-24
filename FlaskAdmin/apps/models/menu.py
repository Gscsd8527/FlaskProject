from exts import db
from .base import BaseModel


class Menu(BaseModel, db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), comment="菜单")
    description = db.Column(db.String(100), comment="菜单说明")

    def __str__(self):
        return "{name} : {description}".format(name=self.title, description=self.description[:20])
