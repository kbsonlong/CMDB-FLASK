# coding:utf-8

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import api
import models

# Init manager object via app object
manager = Manager(api.app)
migrate = Migrate(api.app, models.db)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=api.app,
                db = models.db,
                User = models.User,
                Role = models.Role,
                Authority = models.Authority,
                role_user = models.role_user)

if __name__ == '__main__':
    manager.run()