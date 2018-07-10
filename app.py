from flask import Flask
from flask_script import Manager
from auth_utils import init_auth

from app.user import user
import config

app = Flask(__name__)
manager = Manager(app)

app.register_blueprint(user, url_prefix='/api/user')

app.config['SECRET_KEY'] = config.secret_key

init_auth(app)


@manager.command
def server():
    configs = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    app.run(**configs)


if __name__ == '__main__':
    manager.run()
