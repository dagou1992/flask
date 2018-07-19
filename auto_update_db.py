# coding=utf-8
import atexit
import fcntl
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'auto-upate',
            'func': 'app.task.views:load_task_list',
            'trigger': 'interval',
            'seconds': 60,
        },
    ]


def register_auto_update_db(app):
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        app.config.from_object(Config())
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)
