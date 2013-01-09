from flask import Blueprint, render_template, url_for
from flask_app.models import *
import json
from flask.ext.login import current_user, login_required
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from flask import request, render_template, redirect, flash, make_response, send_file

default = Blueprint('default', __name__)

@default.route('/')
@login_required
def index():   
    return render_template('index.html')

@default.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@default.route('/login', methods=['POST'])
def login_post():
    login = request.form['email']
    # TODO: check for password too.
    u = User.get(login)
    if u:
        login_user(u, remember=request.form.get('remember'))
        flash("login success")
    else:
        flash("Failed login")
    return redirect('/')

@default.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return render_template('login.html'), 404
