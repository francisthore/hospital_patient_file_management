#!/usr/bin/python3
"""Handles API calls for the medical_records model"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from markupsafe import escape
from models.medical_record import MedicalRecord
from models.user import User
from models.staff import Staff
from utilities.decorators import (staff_one_required,
                                  staff_two_required, admin_required)


@app_views.route('/medical_records/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
@staff_two_required
def get_medical_record_by_id(user_id):
    """Retrieves medical record details"""
    user_id = escape(user_id)
    medical_record = storage.get_by_user_id(MedicalRecord, user_id)
    if not medical_record:
        abort(404)
    return jsonify(medical_record.to_dict()), 200


@app_views.route('/medical_records', methods=['GET'], strict_slashes=False)
@staff_two_required
def get_medical_records():
    """Retrieves all medical records"""
    medical_records = storage.all(MedicalRecord)
    medical_records = [medical_record.to_dict()
                       for medical_record in medical_records.values()]
    return jsonify(medical_records), 200


@app_views.route('/medical_records/<string:patient_id>', methods=['DELETE'],
                 strict_slashes=False)
@staff_two_required
def delete_medical_record(patient_id):
    """Deletes a medical record"""
    patient_id = escape(patient_id)
    medical_record = storage.get_by_user_id(MedicalRecord, patient_id)
    if not medical_record:
        abort(404)
    storage.delete(medical_record)
    storage.save()
    return jsonify({}), 200


@app_views.route('/medical_records', methods=['POST'], strict_slashes=False)
@staff_two_required
def create_medical_record():
    """Creates a medical record"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'patient_id' not in data:
        abort(400, 'Missing user_id')
    if 'staff_id' not in data:
        abort(400, 'Missing staff_id')
    if 'diagnosis' not in data:
        abort(400, 'Missing diagnosis')
    if 'prescription' not in data:
        abort(400, 'Missing prescription')
    new_medical_record = MedicalRecord(**data)
    new_medical_record.save()
    return jsonify(new_medical_record.to_dict()), 201


@app_views.route('/medical_records/<string:rec_id>', methods=['PUT'],
                 strict_slashes=False)
@staff_two_required
def update_medical_record(rec_id):
    """Updates a medical record"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    rec_id = escape(rec_id)
    medical_record = storage.get(MedicalRecord, rec_id)
    if not medical_record:
        abort(404)
    for key, value in data.items():
        setattr(medical_record, key, value)
    medical_record.save()
    return jsonify(medical_record.to_dict()), 200
