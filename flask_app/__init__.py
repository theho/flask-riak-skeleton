import os
import logging

# Flask
from flask import Flask,url_for


app = Flask(__name__, static_folder=None)  # Disable static 

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

# Static files
app.static_folder = 'static'  # Enable is back, but the URL rule is still not created 
app.add_url_rule('/static/<path:filename>', 
                      endpoint='static', 
                      view_func=app.send_static_file)

def static(path):
    return url_for('static', filename=path)

@app.context_processor
def inject_static():
    return dict(static=static)

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
# from flask_app.lib.helpers import page_not_found

# Blueprints
from flask_app.controllers.web import web
app.register_blueprint(web, subdomain='www')

from flask_app.controllers.mobile import mobile
app.register_blueprint(mobile, subdomain='m')

from flask_app.controllers.api import api
app.register_blueprint(api, subdomain='api')