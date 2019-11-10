from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run import app
from exts import db
# 导入才能被manger引用到
from models import User

manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app, db)

#添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()