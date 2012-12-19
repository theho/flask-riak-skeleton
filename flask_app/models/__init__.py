
# Model classes can go here

import flask_app.lib.riaky as riaky 
from riakkit import *
from schematics.types import StringType

class User(riaky.Document):
    bucket_name = 'user'
    name = StringType(max_length=10)
    @property
    def username(self):
        return self.key