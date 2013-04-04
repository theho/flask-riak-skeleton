from flask import Blueprint, render_template, jsonify
from flask_app.models import *
import json
from flask.ext.login import current_user, login_required, login_user, logout_user
from flask import request, render_template, redirect, flash, make_response, send_file

api = Blueprint('api', __name__)

# NOTE: Use webserver to block non-https calls to api.

@api.route('/')
def index():   
    return jsonify({'status':'ok'})
