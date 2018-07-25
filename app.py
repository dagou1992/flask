from flask import Flask
from flask_script import Manager
from auth_utils import init_auth

from app.user import user
from app.work import work
from app.task import task
import config
from auto_update_db import register_auto_update_db

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
manager = Manager(app)

app.register_blueprint(user, url_prefix='/api/user')
app.register_blueprint(work, url_prefix='/api/work')
app.register_blueprint(task, url_prefix='/api/task')

app.config['SECRET_KEY'] = config.secret_key

init_auth(app)

register_auto_update_db(app)


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html'), 200


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
