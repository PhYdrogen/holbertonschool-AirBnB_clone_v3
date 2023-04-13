#!/usr/bin/python3
""" App file where flask is launched """
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(err):
    storage.close()


@app.errorhandler(404)
@app.errorhandler(405)
def _handle_api_error(ex):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
