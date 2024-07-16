#!/usr/bin/python3
"""Landing view of the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Gets the current status of our api"""
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Gets the object stats"""
    data = {
        'patients': storage.count('Patient'),
        'staff': storage.count('Staff'),
        'medical_records': storage.count('MedicalRecord'),
        'appointments': storage.count('Appointment'),
        'users': storage.count('User')
    }
    return jsonify(data), 200
