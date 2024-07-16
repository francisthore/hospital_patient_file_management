#!/usr/bin/python3
"""API Entry for the project"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from markupsafe import escape
from models import storage
from flask_wtf import CSRFProtect
import secrets
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('MAIN_API_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = API_KEY
app.register_blueprint(app_views)
CORS(app)


@app.teardown_appcontext
def close_storage(e):
    """Closes storage session when app context
    is teared"""
    storage.close()


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


@app.errorhandler(404)
def not_found(e):
    """Handles the not found 404 error code"""
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(400)
def not_valid_json(e):
    """Handles the not JSON error"""
    return jsonify({'error': 'Not a JSON'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
