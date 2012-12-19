import riak
import json
from schematics.models import Model

riak_client = None

def connect(host=None, port=None, app=None):
    global riak_client

    # flask app object
    if app:  
        conn_settings = {
            # TODO: Include other parameters 
            'host': app.config.get('RIAK_HOST', None),
            'port': int(app.config.get('RIAK_PORT', 0)) or None
        }
        conn_settings = dict([(k, v) for k, v in conn_settings.items() if v])
        riak_client = riak.RiakClient(**conn_settings)
    else:
        raise NotImplementedError('implement host/port connection')

class RiakyException(Exception): 
    pass

class Document(Model):
    '''Wrapper class around schematics.models.Model class
    It basically allow loading and saving to riak'''
    # First cut of document class
    # It is suppose to be as thin as possible
    bucket_name = None

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        self.client = riak_client
        self.robj = None
        self._key = kwargs.get('key')
        self.bucket = self.client.bucket(self.bucket_name)

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.key)

    @property 
    def key(self):
        if self.robj and not self._key:
            self._key = self.robj._key
        return self._key

    @key .setter
    def key(self, value):
        if self._key:
            raise RiakyException, 'Key already defined: %s' % self._key
        self._key = value

    @classmethod
    def get(cls, key):
        '''Get riak object object and deserialised into model'''
        if not cls.bucket_name:
            raise RiakyException, 'bucket is not defined'

        obj = riak_client.bucket(cls.bucket_name).get(key)
        data = obj.get_data()
        if data is None:
            return None
            # m = cls()
        else:
            json_data = json.loads(data)
            m = cls(**json_data)
            m.validate()

        m.robj = obj
        return m

    def save(self):
        '''Save to riak after validate'''
        self.validate()
        if self.robj:
            self.robj.set_data(self.to_json())
        else:
            self.robj = self.bucket.new(key=self.key, data=self.to_json())
        self.robj.store()

    def delete(self):
        if self.robj:
            self.robj.delete()
        return self
