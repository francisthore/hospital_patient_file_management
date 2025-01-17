#!/usr/bin/python3
"""Module to handle admin routes"""
from flask import (Blueprint, render_template, flash,
                   redirect, url_for, abort, request)
from flask_login import current_user
import requests
from utilities.decorators import admin_required
from functools import wraps
from main_app.forms import (AddPatientForm,
                            SearchPatientForm,
                            AddMedicalrecordForm,
                            EditPatientForm, EditMedicalrecordForm)
import json
from markupsafe import escape
from models.patient import Patient
from models.medical_record import MedicalRecord
from models import storage


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET'],
            strict_slashes=False)
@admin_required
def admin_dashboard():
    """Renders the admin dashboard"""
    # Get cookies from session
    session_cookies = request.cookies
    url = 'http://0.0.0.0:5001/api/v1/stats'
    # Pass cookies in the request to api
    with requests.get(url, cookies=session_cookies) as response:
        if response.status_code == 200:
            stats = response.json()
        else:
            stats = {}
    return render_template('admin/admin_dashboard.html',
                           current_user=current_user,
                           stats=stats)


@admin.route('/patients', methods=['GET', 'POST'],
             strict_slashes=False)
@admin_required
def manage_patients():
    """Patient Management Route"""
    form = SearchPatientForm()
    # Handle form after validation
    if form.validate_on_submit():
        id_num = form.id_number.data
        patient = storage.get_by_id_number(Patient, id_num)
        if patient:
            return render_template('admin/manage_patients.html',
                                   current_user=current_user, patient=patient,
                                   form=form)
        else:
            flash("Patient not found, check id number and try again",
                  'danger')
            return redirect(url_for('admin.manage_patients'))
    if form.errors != {}:
        for cat, msg in form.errors.items():
            flash(msg[0], 'danger')
    return render_template('admin/manage_patients.html',
                           current_user=current_user,
                           form=form)


@admin.route('/add_patient', methods=['GET', 'POST'])
@admin_required
def add_patient():
    """Add patient route"""
    form = AddPatientForm()
    session_cookies = request.cookies
    if form.validate_on_submit():
        # Get data from form
        data = {
        'fullname': form.fullname.data,
        'id_number': form.id_number.data,
        'dob': str(form.dob.data),
        'sex': form.sex.data,
        'address': form.address.data,
        'email': form.email.data,
        'cell': form.cell.data
        }
        url = 'http://0.0.0.0:5001/api/v1/patients'
        # Define headers for the request
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': request.cookies.get('csrftoken')
            }
        response = requests.post(url,
                                 cookies=session_cookies,
                                 headers=headers,
                                 data=json.dumps(data)
                                 )
        if response.status_code == 201:
            # Reload storage to get new patient
            storage.reload()
            flash('Patient added successfully', 'success')
            return redirect(url_for('admin.add_patient'))
        else:
            flash('An error occurred. Please try again', 'danger')
            return redirect(url_for('admin.add_patient'))
    if form.errors != {}:
        # Print error messages to frontend
        for category, error_msg in form.errors.items():
            flash(str(error_msg[0]), 'danger')
    return render_template('admin/patients_add.html', form=form, current_user=current_user)


@admin.route('/view_patient/<string:id>', methods=['GET', 'POST'],
             strict_slashes=False)
@admin_required
def view_patient(id):
    """Patient view"""
    id = escape(id)
    form = AddMedicalrecordForm() 
    session_cookies = request.cookies
    url = 'http://0.0.0.0:5001/api/v1/patients/{}'.format(id)
    with requests.get(url, cookies=session_cookies) as response:
        # Get Patient 1st
        if response.status_code == 200:
            patient = response.json()
            # Then handle medical record entry
            if form.validate_on_submit():
                # Get data from form
                data = {
                    'patient_id': id,
                    'staff_id': storage.get_id_by_user_id('Staff', current_user.id),
                    'diagnosis': form.diagnosis.data,
                    'prescription': form.prescription.data
                }
                url = 'http://0.0.0.0:5001/api/v1/medical_records'
                # Define headers for the request
                headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': request.cookies.get('csrftoken')
                    }
                response = requests.post(url, headers=headers,
                                         cookies=session_cookies,
                                         data=json.dumps(data))
                if response.status_code == 201:
                    # Reload storage to get the new medical record
                    storage.reload()
                    url_prefix = 'http://0.0.0.0:5001/api/v1/patients'
                    url_postfix = '/{}/medical_records'.format(id)
                    url = '{}{}'.format(url_prefix, url_postfix)
                    with requests.get(url, cookies=session_cookies) as response:
                        if response.status_code == 200:
                            medical_records = response.json()
                            return render_template('admin/view_patient.html',
                                           medical_records=medical_records,
                                           current_user=current_user,
                                           form=form, patient=patient)
            # Creating two parts of the URL due to length restrictions
            url_prefix = 'http://0.0.0.0:5001/api/v1/patients'
            url_postfix = '/{}/medical_records'.format(id)
            url = '{}{}'.format(url_prefix, url_postfix)
            with requests.get(url, cookies=session_cookies) as response:
                if response.status_code == 200:
                    medical_records = response.json()
                    return render_template('admin/view_patient.html',
                                   patient=patient,
                                   medical_records=medical_records,
                                   current_user=current_user,
                                   form=form)
        flash('Patient not found', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    

@admin.route('/edit_patient/<string:patient_id>', methods=['GET', 'POST'],
             strict_slashes=False)
def edit_patient(patient_id):
    """Edits a patient"""
    form = EditPatientForm()
    session_cookies = request.cookies
    p_id = escape(patient_id)
    patient = storage.get(Patient, p_id)
    if patient is None:
        flash('Patient not found', 'danger')
        abort(404)
    if request.method ==  'GET':
        # Preset form data with patient data
        form.fullname.data = patient.fullname
        form.id_number.data = patient.id_number
        form.dob.data = patient.dob
        form.sex.data = patient.sex
        form.address.data = patient.address
        form.email.data = patient.email
        form.cell.data = patient.cell

        return render_template('admin/edit_patient.html',
                               form=form, patient=patient)

    if form.validate_on_submit():
        # Get data from form
        data = {
        'fullname': form.fullname.data,
        'id_number': form.id_number.data,
        'dob': str(form.dob.data),
        'sex': form.sex.data,
        'address': form.address.data,
        'email': form.email.data,
        'cell': form.cell.data
        }
        url = 'http://0.0.0.0:5001/api/v1/patients/{}'.format(p_id)
        # Define headers for the request
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': request.cookies.get('csrftoken')
            }
        response = requests.put(url,
                                cookies=session_cookies,
                                headers=headers,
                                data=json.dumps(data)
                                )
        if response.status_code == 200:
            # Reload storage to get the updated patient
            storage.reload()
            flash('Patient updated successfully', 'success')
            return redirect(url_for('admin.view_patient', id=p_id))
        else:
            flash('An error occurred. Please try again', 'danger')
            return redirect(url_for('user_profile.profile'))
    if form.errors != {}:
        for category, error_msg in form.errors.items():
            flash(str(error_msg[0]), 'danger')


@admin.route('/edit_medical_record/<string:rec_id>', methods=['GET', 'POST'],
             strict_slashes=False)
@admin_required
def edit_medical_record(rec_id):
    """Edits a medical record"""
    rec_id = escape(rec_id)
    form = EditMedicalrecordForm()
    session_cookies = request.cookies
    # Could improve and use an api call instead
    rec = storage.get(MedicalRecord, rec_id)
    if rec is None:
        flash ("Medical record not found", 'danger')
        abort(404)
    if request.method == 'GET':
        # Preset form data with medical record data
        form.diagnosis.data = rec.diagnosis
        form.prescription.data = rec.prescription

        return render_template('admin/edit_medical_record.html',
                               form=form, rec=rec)
    
    if form.validate_on_submit():
        # Get data from form
        data = {
            'diagnosis': form.diagnosis.data,
            'prescription': form.prescription.data
        }
        url = 'http://0.0.0.0:5001/api/v1/medical_records/{}'.format(rec_id)
        # Define headers for the request
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': request.cookies.get('csrftoken')
            }
        response = requests.put(url,
                                cookies=session_cookies,
                                headers=headers,
                                data=json.dumps(data)
                                )
        if response.status_code == 200:
            storage.reload()
            flash('Record updated successfully', 'success')
            return redirect(url_for('admin.manage_patients'))
        else:
            flash('An error occurred. Please try again', 'danger')
            return redirect(url_for('admin.manage_patients'))
    if form.errors != {}:
        for category, error_msg in form.errors.items():
            flash(str(error_msg[0]), 'danger')
