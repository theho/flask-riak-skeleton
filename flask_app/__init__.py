import os
import logging

# Flask
from flask import Flask

app = Flask(__name__)

# Config
env_to_config = {
    'DEV': 'flask_app.config.DevelopmentConfig',
    'TEST': 'flask_app.config.TestConfig',
    'PROD': 'flask_app.config.ProductionConfig'
}

config = env_to_config[os.getenv('FLASK_ENV')]
app.config.from_object(config)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Setup Riak
import lib.riaky
lib.riaky.connect(app=app)

# Setup Flask-Security
from flask.ext.security import Security
from lib.security import RiakyUserDatastore
from flask_app.models import User, Role
user_datastore = RiakyUserDatastore(lib.riaky.riak_client, User, Role)
security = Security(app, user_datastore)

# Helpers
from flask_app.lib.helpers import page_not_found

# Blueprints    
from flask_app.controllers.default import default
app.register_blueprint(default)
