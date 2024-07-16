#!/usr/bin/python3
"""Module to handle admin routes"""
from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
import requests
from utilities.decorators import admin_required
from functools import wraps
from main_app.forms import AddPatientForm, SearchPatientForm, AddMedicalrecordForm
import json
from markupsafe import escape
from models.patient import Patient
from models import storage


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/', methods=['GET'],
            strict_slashes=False)
@admin_required
def admin_dashboard():
    """Renders the admin dashboard"""
    url = 'http://0.0.0.0:5000/api/v1/stats'
    with requests.get(url) as response:
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
    if form.validate_on_submit():
        id_num = form.id_number.data
        patient = storage.get_by_id_number(Patient, id_num)
        if patient:
            return render_template('admin/manage_patients.html',
                                   current_user=current_user, patient=patient,
                                   form=form)
        else:
            flash("Patient not found, check id number and try again", 'danger')
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
    if form.validate_on_submit():
        data = {
        'fullname': form.fullname.data,
        'id_number': form.id_number.data,
        'dob': str(form.dob.data),
        'sex': form.sex.data,
        'address': form.address.data,
        'email': form.email.data,
        'cell': form.cell.data
        }
        url = 'http://0.0.0.0:5000/api/v1/patients'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            storage.reload()
            flash('Patient added successfully', 'success')
            return redirect(url_for('admin.add_patient'))
        else:
            flash('An error occurred. Please try again', 'danger')
    if form.errors != {}:
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
    
    url = 'http://0.0.0.0:5000/api/v1/patients/{}'.format(id)
    with requests.get(url) as response:
        # Get Patient 1st
        if response.status_code == 200:
            patient = response.json()
            if form.validate_on_submit():
                data = {
                    'patient_id': id,
                    'staff_id': storage.get_id_by_user_id('Staff', current_user.id),
                    'diagnosis': form.diagnosis.data,
                    'prescription': form.prescription.data
                }
                url = 'http://0.0.0.0:5000/api/v1/medical_records'
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers,
                                         data=json.dumps(data))
                if response.status_code == 201:
                    storage.reload()
                    url_prefix = 'http://0.0.0.0:5000/api/v1/patients'
                    url_postfix = '/{}/medical_records'.format(id)
                    url = '{}{}'.format(url_prefix, url_postfix)
                    with requests.get(url) as response:
                        if response.status_code == 200:
                            medical_records = response.json()
                            return render_template('admin/view_patient.html',
                                           medical_records=medical_records,
                                           current_user=current_user,
                                           form=form, patient=patient)
            url_prefix = 'http://0.0.0.0:5000/api/v1/patients'
            url_postfix = '/{}/medical_records'.format(id)
            url = '{}{}'.format(url_prefix, url_postfix)
            with requests.get(url) as response:
                if response.status_code == 200:
                    medical_records = response.json()
                    return render_template('admin/view_patient.html',
                                   patient=patient,
                                   medical_records=medical_records,
                                   current_user=current_user,
                                   form=form)
        flash('Patient not found', 'danger')
        return redirect(url_for('admin.admin_dashboard'))   
