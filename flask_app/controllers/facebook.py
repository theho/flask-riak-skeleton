from flask import g, Blueprint, redirect, session
from flask_oauth import OAuth
from flask_app import app
from models import *

mod = Blueprint('facebook', __name__, url_prefix='/oauth/facebook')

facebook = oauth.remote_app('facebook',
    base_url = 'https://graph.facebook.com/',
    request_token_url = None,
    access_token_url = '/oauth/access_token',
    authorize_url = 'https://facebook.com/dialog/oauth',
    consumer_key = app.config.FACEBOOK_APP_ID,
    consumer_secret = app.config.FACEBOOK_APP_SECRET,
    request_token_params = { 'scope': 'email' }
)

@facebook.tokengetter 
def facebook_token():
    if g.user:
        service = g.user.service('facebook')
        if service:
            return service['token'], service['secret']

@mod.route ('/signin')
def facebook_signin():
    return facebook.authorize(callback='http://hogatu.com/oauth/facebook/authorized')

@mod.route ('/authorized')
@facebook.authorized_handler 
def facebook_authorized(resp):
    print resp
    print('facebook', 1,
                     resp['access_token'])
    return redirect('/')

