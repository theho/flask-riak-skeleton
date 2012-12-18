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


# Setup Riak
import lib.riaky
lib.riaky.connect(app)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Helpers
from flask_app.lib.helpers import page_not_found

# Blueprints    
from flask_app.controllers.default import default
app.register_blueprint(default)
