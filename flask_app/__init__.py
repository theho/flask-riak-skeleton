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


# Helpers
from flask_app.lib.helpers import page_not_found

# Blueprints    
from flask_app.controllers.default import default
app.register_blueprint(default)
