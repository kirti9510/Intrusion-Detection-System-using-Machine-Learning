from flask import Flask
from celery import Celery
from hodor.blueprints.page import page
from hodor.blueprints.pcap import pcap

"""
    http://stackoverflow.com/questions/26281935/simple-network-udp-listen-in-flask-or-pyramid
"""

def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :re turn: Celery app
    """
    CELERY_TASK_LIST = [ 'hodor.blueprints.pcap.tasks' ]
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    CELERY_APP = create_celery_app
    app.register_blueprint(page)
    app.register_blueprint(pcap)
    return app
