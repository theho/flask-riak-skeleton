import riak
import json
import copy
from schematics.models import Model
from crdt.sets import LWWSet

######
# THIS IS NOT READY FOR PROD!  Pre-Alpha code!!
#####

riak_client = None

def connect(host=None, port=None, app=None):
    global riak_client

    # flask app object
    if app:  
        conn_settings = {
            # TODO: Include other parameters 
            'host': app.config.get('RIAK_HOST', None),
            'port': int(app.config.get('RIAK_PORT', 0)) or None,
        }
        if app.config.get('RIAK_PBC') and app.config.get('RIAK_PORT_PB'):
            conn_settings['transport_class']= riak.RiakPbcTransport
            conn_settings['port'] = app.config.get('RIAK_PORT_PB')

        conn_settings = dict([(k, v) for k, v in conn_settings.items() if v])
        print conn_settings
        riak_client = riak.RiakClient(**conn_settings)
    else:
        raise NotImplementedError('implement host/port connection')

class RiakyException(Exception): 
    pass



class Document(Model):

    bucket_name = None
    _search = True

    def __new__(cls, *args, **kwargs):
        cls.client = riak_client
        cls.bucket = cls.client.bucket(cls.bucket_name)
        if not cls.bucket.search_enabled() and cls._search:
            print 'Enabling search to bucket %s' % cls.bucket_name
            cls.bucket.enable_search()

        return super(Document, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        self.riak_object = None

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.key)

    @property 
    def key(self):
        if self.riak_object:
            return self.riak_object._key
        else:
            return None
    id = key

    @classmethod
    def get(cls, key):
        '''Get riak object object and deserialised into model'''
        if not cls.bucket_name:
            raise RiakyException, 'bucket is not defined'

        riak_obj = riak_client.bucket(cls.bucket_name).get(key)
        if riak_obj.has_siblings():
            riak_obj, cls_obj = cls.merge_siblings(riak_obj)
        elif not riak_obj or not riak_obj.exists():
            print 'not found'
            riak_obj = riak_client.bucket(cls.bucket_name).new(key=key)
            cls_obj = cls.from_riak(riak_obj)
        elif riak_obj.exists():
            print 'found'
            cls_obj = cls.from_riak(riak_obj)
        else:
            raise Exception, 'What else is there really???'

        return cls_obj

    class Abort(Exception):
        pass

    def abort(self):
        raise self.Abort()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Swallow up aborts without committing
        if exc_type is self.Abort:
            return True

        # If no exception happened within the with block, commit the
        # object
        if exc_type is None:
            self.save()

        # Otherwise, return False which tells Python to reraise any exceptions
        return False

    @classmethod
    def merge(cls, first, second):
        for f in cls.crdt_fields():
            if hasattr(first, f) and hasattr(second, f):
                new_f = getattr(first, f).__class__.merge(getattr(first, f), getattr(second, f))
                setattr(second, f, new_f)
        return second

    @classmethod
    def merge_siblings(cls, riak_obj):
        siblings = riak_obj.get_siblings()
        #
        # In Riak 1.0, tombstone siblings comeback with no data so we need
        # to filter those out.  This occurs on concurrent DELETE and PUTs
        # I am not sure
        siblings = [obj for obj in siblings
                    if obj.get_data() != ""]

        first = siblings[0]
        others = siblings[1:]

        # Create the starting point using the first sibling
        crdt = cls.from_riak(first)

        # Merge the other siblings to the first one
        for other in others:
            other_crdt = cls.from_riak(other)
            crdt = cls.merge(crdt, other_crdt)

        # Return one of the siblings because they have the VClock value
        return first, crdt

    def populate(self, values):
        ### Loop over fields in model
        for attr_name, attr_value in self._fields.items():
            # Use default value if present

            field_name = attr_name
            if field_name in values:
                field_value = values[field_name]
                setattr(self, field_name, field_value)

        for cfield in self.__class__.crdt_fields():
            if cfield in values:
                field_value = values[cfield]
                setattr(self, cfield, field_value)


    @classmethod
    def from_riak(cls, riak_obj):
        data = riak_obj.get_data() or {}

        crdt = dict()
        for f in cls.crdt_fields():
            if f in data:
                crdt[f] = copy.deepcopy(data[f])
                del data[f]
        m = cls(**data)

        for k, v in crdt.iteritems():
            f = getattr(m, k)
            setattr(m, k, f.from_payload(v))
                
        m.validate()
        m.riak_object = riak_obj
        return m

    @classmethod
    def crdt_fields(cls):
        f = list()
        for attr in dir(cls):
            attrib = getattr(cls, attr)
            if hasattr(attrib, 'payload'):
                f.append(attr)
        return f

    def save(self):
        '''Save to riak after validate'''
        self.validate()
        # if not self.bucket.search_enabled() and self._search:
            # self.bucket.enable_search()
        data_struct = json.loads(self.to_json())

        for f in self.__class__.crdt_fields():
            data_struct[f] = getattr(self, f).payload
        
        if self.riak_object:
            self.riak_object.set_data(data_struct)
        else:
            self.riak_object = self.bucket.new(key=self.key, data=data_struct)
        self.riak_object.store()


    def delete(self):
        if self.riak_object:
            self.riak_object.delete()

    @classmethod
    def search(cls, qry):
        print 'Query: %s on Bucket: %s', qry, cls.bucket_name
        search_query = riak_client.search(cls.bucket_name, qry)

        for result in search_query.run():
            print 'FOUND'
            obj = result.get()
            data = obj.get_data()
            # json_data = json.loads(data)
            m = cls.from_riak(obj)
            yield m

    def add_link(self, other_doc, tag=None, reciprocal=True):

        self.riak_object.add_link(other_doc.riak_object, tag=tag)
        if reciprocal:
            other_doc.riak_object.add_link(self.riak_object, tag=tag)
            other_doc.save()
        return self.save()

    def get_links(self, tag=None):
        return [link for link in self.riak_object.get_links() if tag is None or link.get_tag()==tag]

    def remove_link(self, other_doc, tag=None, reciprocal=False):
        if reciprocal:
            other_doc.riak_object.remove_link(self.riak_object, tag=tag)
        return self.riak_object.remove_link(other_doc.riak_object, tag=tag)


