import riak
import json
from schematics.models import Model

db = None
def connect(app):
    global db
    conn_settings = {
        # TODO: Include other parameters 
        'host': app.config.get('RIAK_HOST', None),
        'port': int(app.config.get('RIAK_PORT', 0)) or None
    }
    conn_settings = dict([(k, v) for k, v in conn_settings.items() if v])
    db = riak.RiakClient(**conn_settings)

class RiakyException(Exception): 
    pass

class RiakModel(Model):
    # First cut of generic model class
    # It is suppose to be as thin as possible
    bucket = None
    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)

    @classmethod
    def get(cls, key):
        if not cls.bucket:
            raise RiakyException, 'bucket is not defined'

        _obj = db.bucket(cls.bucket).get(key)
        if _obj.get_data() is None:
            m = cls()
        else:
            data = json.loads(_obj.get_data())
            m = cls(**data)
            m.validate()

        m._obj = _obj
        m._key = key
        return m

    def store(self):
        self.validate()
        if self._obj:
            self._obj.set_data(self.to_json())
        else:
            self._obj = db.bucket(self.bucket).new(self._key, self.to_json())
        obj.store()
    

