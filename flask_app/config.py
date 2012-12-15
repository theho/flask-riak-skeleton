# http://flask.pocoo.org/docs/config/#development-production

class Config(object):
    SECRET_KEY = '{some very secret key that you should never share}'
    SITE_NAME = '{SITE_NAME}'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class TestConfig(Config):
    DEBUG = False
    TESTING = True