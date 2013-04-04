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

# If running on local pc (mac), load DEV config
import socket
hostname = socket.gethostname()
if 'mac' in hostname:
    config = env_to_config['DEV']
else:
    config = env_to_config['PROD']

app.config.from_object(config)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Setup Riak
import lib.riaky
lib.riaky.connect(app=app)

# Login Manager
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, AnonymousUser,
                            confirm_login, fresh_login_required)
from models import User


login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message = u"Please log in to access this page."


@login_manager.user_loader
def load_user(id):
    print 'load_user', id, id.__class__
    user = User.get(id)
    print 'loaded', user, user.key
    return user

login_manager.setup_app(app)


# Helpers
from flask_app.lib.helpers import page_not_found

# Blueprints
from flask_app.controllers.default import web
app.register_blueprint(web)

from flask_app.controllers.default import mobile
app.register_blueprint(mobile)