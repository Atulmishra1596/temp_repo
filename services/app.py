#!/usr/bin/env python3
import os
import connexion
import multiprocessing
import gunicorn.app.base
from flask import request
from connexion.resolver import RestyResolver
from flask_cors import CORS
import logging
import traceback
from logging.config import fileConfig
from dotenv import load_dotenv
from flask_session import Session
load_dotenv()


# logging.basicConfig(
#     format='[%(levelname)s] %(asctime)s.%(msecs)03d [%(threadName)s]
#  %(module)s : %(message)s',
#     level=logging.INFO
# )
LOGGER = logging.getLogger(__name__)
os.environ['LOG_DIR'] = os.path.join(os.path.dirname(__file__), 'logs')
fileConfig(os.path.join(os.environ['LOG_DIR'], 'jnj_logging.conf'), disable_existing_loggers=False)

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('jnj_python_api.yaml', resolver=RestyResolver('endpoints'))
APPLICATION_HOST = os.getenv('APPLICATION_HOST', 'http://localhost')
whitelist = APPLICATION_HOST.split(',')
CORS(app.app, resources={r"/*": {"origins": whitelist}})
app.app.config["SESSION_PERMANENT"] = True
app.app.config["SESSION_TYPE"] = "filesystem"

Session(app.app)



@app.app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        LOGGER.error('%s %s %s %s %s',
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     response.status)
    return response


@app.app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    tb = traceback.format_exc()
    LOGGER.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 tb)
    return "Internal Server Error", 500


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '0.0.0.0:9091',
        'workers': number_of_workers(),
        'timeout': 600,
    }
    StandaloneApplication(app.app, options).run()
