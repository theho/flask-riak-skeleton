
# Model classes can go here

from flask_app.lib.riaky import Document
from schematics.types import StringType, EmailType, BooleanType, DateTimeType
from schematics.types.compound import ListType
from flask.ext.security import UserMixin, RoleMixin

class User(Document, UserMixin):
    bucket_name = 'user'

    id = Document.key
    email = EmailType()
    name = StringType(max_length=38)
    password = StringType(max_length=8)
    active = BooleanType(default=True)
    confirmed_at = DateTimeType()
    roles = ListType(StringType()) 

    @property
    def username(self):
        return self.key

class Role(Document, RoleMixin):

    id = Document.key
    bucket_name = 'role'
    name = StringType(max_length=8)
    description = StringType(max_length=208)

# class Role(riaky.Document, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))

# class User(riaky.Document, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     active = db.Column(db.Boolean())
#     confirmed_at = db.Column(db.DateTime())
#     roles = db.relationship('Role', secondary=roles_users,
#                             backref=db.backref('users', lazy='dynamic'))