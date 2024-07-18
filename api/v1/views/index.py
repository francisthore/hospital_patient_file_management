#!/usr/bin/python3
"""Landing view of the api"""
from api.v1.views import app_views
from flask import jsonify
from flask_login import current_user
from models import storage
from utilities.decorators import (staff_one_required,
                                  staff_two_required, admin_required)

@app_views.route('/test', methods=['GET'], strict_slashes=False)
def test_route():
    if current_user.is_authenticated:
        return jsonify({'message': f'Hello, {current_user.role}'}), 200
    else:
        return jsonify({'message': 'User not authenticated'}), 403

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Gets the current status of our api"""
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
@staff_one_required
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
