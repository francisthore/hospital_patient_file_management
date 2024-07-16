#!/usr/bin/python3
"""Handles api CRUD for the patients model"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from markupsafe import escape
from models.patient import Patient


@app_views.route('/patients', methods=['GET'], strict_slashes=False)
def get_patients():
    """Retrives and serves all patients"""
    data = [o.to_dict() for o in storage.all('Patient').values()]
    return jsonify(data), 200


@app_views.route('/patients/<string:patient_id>',
                 methods=['GET'], strict_slashes=False)
def get_patient(patient_id):
    """Retrieves one patient from db"""
    p_id = escape(patient_id)
    patient = storage.get('Patient', p_id)
    if patient is None:
        abort(404)
    return jsonify(patient.to_dict()), 200


@app_views.route('/patients/<string:patient_id>/medical_records',
                 methods=['GET'], strict_slashes=False)
def get_patient_medical_records(patient_id):
    """Retrieves one patient from db and their records"""
    p_id = escape(patient_id)
    patient = storage.get('Patient', p_id)
    if patient is None:
        abort(404)
    medical_records = [record.to_dict() for record in patient.medical_records]
    return jsonify({'medical_records': medical_records}), 200


@app_views.route('/patients/<string:patient_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_patient(patient_id):
    """Deletes a patient from storage"""
    p_id = escape(patient_id)
    patient = storage.get('Patient', p_id)
    if patient is None:
        abort(404)
    storage.delete(patient)
    storage.save()
    return jsonify({}), 200


@app_views.route('/patients', methods=['POST'], strict_slashes=False)
def create_patient():
    """Creates a patient"""
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not data:
        abort(400)
    required_fields = ['fullname', 'id_number', 'dob', 'sex', 'address']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify(
            {"error": "Missing fields: " + ", ".join(missing_fields)}
            ), 400
    try:
        new_patient = Patient(**data)
        new_patient.save()
        return jsonify(new_patient.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app_views.route('/patients/<string:patient_id>', methods=['PUT'],
                 strict_slashes=False)
def update_patient(patient_id):
    """Updates a patient's details"""
    p_id = escape(patient_id)
    patient = storage.get(Patient, p_id)
    if not patient:
        abort(404)
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if not data:
        abort(400)
    for k, v in data.items():
        ignore = ['id', 'created_at', 'updated_at']
        if k not in ignore:
            setattr(patient, k, v)
    patient.save()
    return jsonify(patient.to_dict()), 200
