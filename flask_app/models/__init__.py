
# Model classes can go here

from flask_app.lib.riaky import RiakModel
from schematics.types import StringType

class User(RiakModel):
    bucket = 'user'
    name = StringType(max_length=10)

