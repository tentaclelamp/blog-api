from settings import BlogSetting
from flask import Flask

from app.api_1_0.api import db, api_bp
from models.model import model
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from models.model import User
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(BlogSetting)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

app.register_blueprint(api_bp)
app.register_blueprint(model)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.config.from_object(BlogSetting)
    manager.run()
