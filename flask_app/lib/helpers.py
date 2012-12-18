from flask import render_template
from flask_app import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
