#!/usr/bin/python3
"""API Entry for the project"""
from api.v1.views import app_views
from flask import Blueprint, jsonify
from flask_cors import CORS
from markupsafe import escape
from models import storage
from models.user import User
import os
from dotenv import load_dotenv

api = Blueprint('api', __name__)


@api.teardown_app_request
def close_storage(e):
    """Closes storage session when app context
    is teared"""
    storage.close()


@api.after_request
def add_header(response):
    """Adds headers to response"""
    response.cache_control.no_store = True
    return response


@api.errorhandler(404)
def not_found(e):
    """Handles the not found 404 error code"""
    return jsonify({'error': 'Not Found'}), 404


@api.errorhandler(400)
def not_valid_json(e):
    """Handles the not JSON error"""
    return jsonify({'error': 'Not a JSON'}), 400


@api.errorhandler(403)
def not_valid_json(e):
    """Handles the not JSON error"""
    return jsonify({'error': 'Forbidden'}), 403


api.register_blueprint(app_views, url_prefix='/api/v1')
