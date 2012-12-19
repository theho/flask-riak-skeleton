from flask_security.datastore import *

class RiakyDatastore(Datastore):
    def put(self, model):
        model.save()
        return model

    def delete(self, model):
        model.delete()


class RiakyUserDatastore(RiakyDatastore, UserDatastore):
    """A Riaky datastore implementation for Flask-Security that assumes
    the use of the Flask-MongoEngine extension.
    """
    def __init__(self, db, user_model, role_model):
        RiakyDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def find_user(self, **kwargs):
        key = kwargs.get('email') or kwargs.get('id')

        if key:
            u = self.user_model.get(key)
            return u
        raise Exception, 'Unsupported query string: %s' % kwargs


    def find_role(self, role):
        return self.role_model.get(role)