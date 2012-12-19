from flask import Blueprint, render_template
from flask_app.models import *
import json

default = Blueprint('default', __name__)

from flask_security.decorators import login_required


@default.route('/')
@login_required
def index():   
    return render_template('index.html')