# Model classes can go here

from flask_app import app
from flask_app.lib.riaky import Document
from schematics.types import StringType, EmailType, BooleanType, DateTimeType
from schematics.types.compound import ListType
from flask.ext.login import UserMixin
from crdt.sets import LWWSet
from crdt.base import StateCRDT


class User(Document, UserMixin):
    bucket_name = '%s.%s' % (app.config['RIAK_DB_PREFIX'], 'user')
    name = StringType()
    email = EmailType()