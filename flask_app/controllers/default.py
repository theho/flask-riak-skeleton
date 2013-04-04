from flask import Blueprint, render_template
from flask_app.models import *
import json
from flask.ext.login import current_user, login_required, login_user, logout_user
from flask import request, render_template, redirect, flash, make_response, send_file

default = Blueprint('default', __name__)

@default.route('/')
def index():   
    return render_template('index.html')


@default.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@default.route('/login', methods=['POST'])
def login_post():
    login = request.form['email']
    # TODO: check for password too.
    flash("login success: %s" % login)
    return redirect('/')

@default.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return render_template('login.html'), 404