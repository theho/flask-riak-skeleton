# http://flask.pocoo.org/docs/config/#development-production

class Config(object):
    SECRET_KEY = '{some very secret key that you should never share}'
    SITE_NAME = '{SITE_NAME}'

    RIAK_DB_PREFIX = 'clique'
    SERVER_NAME='hogatu.com'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    PORT=80
    DOMAIN = 'somedomain.com'

    RIAK_HOST = '123.123.123.123'
    RIAK_PORT = 8098

    # Protobuf port
    RIAK_PORT_PB = 8087
    RIAK_PBC = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    RIAK_HOST = '127.0.0.1'
    RIAK_PORT = 8091
    DOMAIN = 'testdomain.com'
    # Protobuf port
    # RIAK_PORT_PB = 8087
    RIAK_PBC = True
    PORT=80


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    PORT=80