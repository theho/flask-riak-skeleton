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
        # TODO: tidy up some search code
        for f, v in kwargs.iteritems():
            if v:
                if f == 'id':
                    u = self.user_model.get(v)
                    return u
                else:
                    # bit of a hack
                    # TODO: include multiple field search
                    qry = '%s:%s' % (f, str(v))
                    for u in self.user_model.search(qry):
                        return u
            # break
        return None

    def find_role(self, role):
        return None
        # return self.role_model.get(role)