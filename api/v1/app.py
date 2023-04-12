#!/usr/bin/python3
""" App file where flask is launched """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(err):
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    app.run(debug=True, host=host, port=5050, threaded=True)
