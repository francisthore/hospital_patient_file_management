#!/usr/bin/python3
"""Handles authentication routes"""
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from models import storage
from markupsafe import escape
from main_app.forms import RegistrationForm, LoginForm, StaffRegistrationForm, VerifyEmailForm
from models.user import User
from models.staff import Staff
from flask import Blueprint
import json
from utilities.email import send_verification_email
import requests

auth = Blueprint('auth', __name__)

login_manager = LoginManager()

@auth.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """Registers a user"""
    if current_user.is_authenticated:
        return redirect(url_for('user_profile.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        }
        url = 'http://0.0.0.0:5000/api/v1/users'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            flash('Account created successfully, check your email', 'success')
            storage.reload()
            user_id = response.json()['id']
            user = storage.get(User, user_id)
            subject = "Verify Your Email Address"
            send_verification_email(user.email, subject, user.username,
                                user.verification_token)
            if user:
                login_user(user)
                return redirect(url_for('auth.verify_email'))

        elif response.status_code == 400:
            flash('Username or email already in use', 'danger')
        else:
            flash('An error occurred. Please try again', 'danger')
    if form.errors != {}:
        for category, error_msg in form.errors.items():
            flash(str(error_msg[0]), 'danger')
    return render_template('register.html', title='Register', form=form)


@auth.route('/register_staff', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def register_staff():
    """Registers a staff member and associates with user"""
    form = StaffRegistrationForm()
    if form.validate_on_submit():
        data = {
        'fullname': form.fullname.data,
        'id_number': form.id_number.data,
        'dob': str(form.dob.data),
        'sex': form.sex.data,
        'address': form.address.data,
        'email': form.email.data,
        'cell': form.cell.data,
        'user_id': current_user.id
        }
        url = 'http://0.0.0.0:5000/api/v1/staff'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            flash('Staff member registered successfully', 'success')
            return redirect(url_for('user_profile.profile'))
        else:
            flash('An error occurred. Please try again', 'danger')    
        
    return render_template('register_staff.html',
                           current_user=current_user,
                           form=form)

@auth.route('/verify', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def verify_email():
    form = VerifyEmailForm()   

    
    if form.validate_on_submit():
        token = form.v_token.data
        user = storage.get_user_by_verification_token(token)
        if not user:
            flash('Invalid or expired verification token. Please request a new one.', 'error')
            return redirect(url_for('auth.login'))
        user.verified = True
        user.verification_token = None
        storage.save()
        flash('Email verification successful!', 'success')
        return redirect(url_for('auth.register_staff'))
    
    return render_template('verify_email.html', form=form)



@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Authenticates a user and signs them into the system"""
    if current_user.is_authenticated:
        return redirect(url_for('user_profile.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.get_user(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'staff_one' or current_user.role == 'staff_two':
            return redirect(url_for('staff_r.staff_dashboard'))
        else:
            return redirect(url_for('user_profile.profile'))
    
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logs a user out"""
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('auth.login'))
