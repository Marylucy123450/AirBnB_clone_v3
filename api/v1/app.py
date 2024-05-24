#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template
from models import storage
import os

# Global Flask Application Variable: app
app = Flask(__name__)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# Allow CORS for all domains on all routes
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# global strict slashes
app.url_map.strict_slashes = False

# begin flask page rendering


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors
    """
    code = 404
    message = {'error': "Not found"}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # flask server environmental setup
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)

    # start Flask app
    app.run(host=host, port=port, threaded=True)
