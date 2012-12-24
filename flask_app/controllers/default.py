from flask import Blueprint, render_template
from flask_app.models import *
import json

default = Blueprint('default', __name__)

@default.route('/')
# @login_required
def index():   
    return render_template('index.html')

# @default.route('/aaa')
# def aa():   
#     return render_template('index.html')

    

