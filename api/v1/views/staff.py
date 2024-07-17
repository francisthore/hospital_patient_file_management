#!/usr/python3
"""Handles API calls for the staff model"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from flask_login import login_required
from models import storage
from markupsafe import escape
from models.staff import Staff
from models.user import User
from utilities.decorators import (staff_one_required,
                                  staff_two_required, admin_required)


@app_views.route('/staff/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
@staff_one_required
def get_staff_by_id(user_id):
    """Retrieves staff member's details"""
    user_id = escape(user_id)
    staff = storage.get_by_user_id(Staff, user_id)
    if not staff:
        abort(404)
    return jsonify(staff.to_dict()), 200


@app_views.route('/staff', methods=['GET'], strict_slashes=False)
@staff_one_required
def get_staff():
    """Retrieves all staff members"""
    staff = storage.all(Staff)
    staff = [staff.to_dict() for staff in staff.values()]
    return jsonify(staff), 200


@app_views.route('/staff/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
@admin_required
def delete_staff(user_id):
    """Deletes a staff member"""
    user_id = escape(user_id)
    staff = storage.get_by_user_id(Staff, user_id)
    if not staff:
        abort(404)
    storage.delete(staff)
    storage.save()
    return jsonify({}), 200


@app_views.route('/staff', methods=['POST'], strict_slashes=False)
@login_required
def create_staff():
    """Creates a new staff member"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'fullname' not in data:
        abort(400, 'Missing fullname')
    if 'id_number' not in data:
        abort(400, 'Missing id_number')
    if 'dob' not in data:
        abort(400, 'Missing dob')
    if 'sex' not in data:
        abort(400, 'Missing sex')
    if 'address' not in data:
        abort(400, 'Missing address')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'cell' not in data:
        abort(400, 'Missing cell')
    user_id = escape(data['user_id'])
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    new_staff = Staff(**data)
    new_staff.save()

    return jsonify(new_staff.to_dict()), 201


@app_views.route('/staff/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
@staff_one_required
def update_staff(user_id):
    """Updates a staff member"""
    user_id = escape(user_id)
    staff = storage.get(Staff, user_id)
    if not staff:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['fullname', 'id_number', 'dob',
                       'sex', 'address', 'email', 'cell']:
            abort(400, 'Invalid field')
        setattr(staff, key, value)
    storage.save()

    return jsonify(staff.to_dict()), 200


@app_views.route('/staff/<string:user_id>/appointments', methods=['GET'],
                 strict_slashes=False)
@staff_one_required
def get_staff_appointments(user_id):
    """Retrieves all appointments for a staff member"""
    user_id = escape(user_id)
    staff = storage.get_by_user_id(Staff, user_id)
    if not staff:
        abort(404)
    appointments = storage.get_appointments(staff)
    appointments = [appointment.to_dict() for appointment in appointments]
    return jsonify(appointments), 200
