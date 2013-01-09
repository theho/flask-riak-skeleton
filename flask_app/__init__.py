import os
import logging
from flask_mail import Mail

# Flask
from flask import Flask

app = Flask(__name__)
mail = Mail(app)

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

# Login Manager
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, AnonymousUser,
                            confirm_login, fresh_login_required)
from models import User

# class Anonymous(AnonymousUser):
#     name = u"Anonymous"

login_manager = LoginManager()
# login_manager.anonymous_user = Anonymous
login_manager.login_view = "/login"
login_manager.login_message = u"Please log in to access this page."
# login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    user = User.get(id)
    return user

login_manager.setup_app(app)


# Helpers
from flask_app.lib.helpers import page_not_found

# Blueprints    
from flask_app.controllers.default import default
app.register_blueprint(default)
from flask_app.controllers.oauth.facebook import mod
app.register_blueprint(mod)