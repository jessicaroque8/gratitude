import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from resources import api
from models import db, ma, migrate



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
    else:
        # load the test config if passed in
        app.config.from_pyfile(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app
