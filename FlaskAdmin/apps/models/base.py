from exts import db
from datetime import datetime


class BaseModel(db.Model):
    """公共字段"""
    __abstract__ = True
    is_deleted = db.Column(db.Boolean, default=False, comment="是否删除")
    create_time = db.Column(db.DateTime, index=True, default=datetime.now(), comment='插数据结果：每条记录创建的当前时间')
    update_time = db.Column(db.DateTime, index=True, default=datetime.now(), comment='每条记录更新的当前时间')
