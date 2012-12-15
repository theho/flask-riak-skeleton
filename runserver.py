from flask_app import app

if __name__ == '__main__':
    if app.debug:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0')

