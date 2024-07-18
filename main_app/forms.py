#!/usr/python3
"""Module to handle form creation"""
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import (TextAreaField, StringField,
                     PasswordField, IntegerField, RadioField,
                     SubmitField, DateField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo,
                                ValidationError, Length)
from models import storage
import re
from flask import current_app as app


class RegistrationForm(FlaskForm):
    """Class representing a registration form object"""
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Checks if username is not already in db"""
        if storage.check_username(username.data):
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        """Checks if email is not already in db"""
        if storage.check_email(email.data):
            raise ValidationError('Email is already registered')

    def validate_password(self, password):
        """Checks if password meets complexity requirements"""
        password = password.data
        uppercase_req = r'[A-Z]'
        lowercase_req = r'[a-z]'
        digit_req = r'\d'
        special_char_req = r'[!@#$%^&*(),.?":{}|<>]'

        if not re.search(uppercase_req, password):
            raise ValidationError('Password must contain at least 1 CAPS')
        if not re.search(lowercase_req, password):
            raise ValidationError("Password must have at least 1 lowercase")
        if not re.search(digit_req, password):
            raise ValidationError('Password must have at least 1 digit')
        if not re.search(special_char_req, password):
            raise ValidationError('Password must have at least 1 special char')


class StaffRegistrationForm(FlaskForm):
    """Creates a Staff registration form fields"""
    fullname = StringField('Fullname', validators=[DataRequired()])
    id_number = StringField('ID Number', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()],
                    format='%Y-%m-%d')
    sex = RadioField('Sex', validators=[DataRequired()],
                     choices=['Male', 'Female'])
    address = TextAreaField('Address', validators=[DataRequired(),
                                                   Length(min=2, max=256)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cell = IntegerField('Cell', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditStaffForm(FlaskForm):
    """Creates a Staff edit form fields"""
    fullname = StringField('Fullname', validators=[DataRequired()])
    id_number = StringField('ID Number', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()],
                    format='%Y-%m-%d')
    sex = RadioField('Sex', validators=[DataRequired()],
                     choices=['Male', 'Female'])
    address = TextAreaField('Address', validators=[DataRequired(),
                                                   Length(min=2, max=256)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cell = IntegerField('Cell', validators=[DataRequired()])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    """Creates a login form fields"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign In')


class VerifyEmailForm(FlaskForm):
    """Creates a verify email form"""
    v_token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Verify')


class AddPatientForm(FlaskForm):
    """Creates a form to add a patient"""
    fullname = StringField('Fullname', validators=[DataRequired()])
    id_number = StringField('ID Number', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()],
                    format='%Y-%m-%d')
    sex = RadioField('Sex', validators=[DataRequired()],
                     choices=['Male', 'Female'])
    address = TextAreaField('Address', validators=[DataRequired(),
                                                   Length(min=2, max=256)])
    email = StringField('Email', validators=[Email()])
    cell = IntegerField('Cell', validators=[])
    submit = SubmitField('Add Patient')


class EditPatientForm(FlaskForm):
    """Creates a form to edit a patient"""
    fullname = StringField('Fullname', validators=[DataRequired()])
    id_number = StringField('ID Number', validators=[DataRequired()])
    dob = DateField('DOB', validators=[DataRequired()],
                    format='%Y-%m-%d')
    sex = RadioField('Sex', validators=[DataRequired()],
                     choices=['Male', 'Female'])
    address = TextAreaField('Address', validators=[DataRequired(),
                                                   Length(min=2, max=256)])
    email = StringField('Email', validators=[Email()])
    cell = IntegerField('Cell', validators=[])
    submit = SubmitField('Edit Patient')

class SearchPatientForm(FlaskForm):
    """Creates a form to search patient"""
    id_number = StringField('Identity Number', validators=[DataRequired()])
    submit = SubmitField('Search')


class AddMedicalrecordForm(FlaskForm):
    """Create a form to add medical record"""
    diagnosis = TextAreaField('Diagnosis',
                              validators=[DataRequired(),
                                          Length(min=10, max=1024)])

    prescription = TextAreaField('Prescription',
                                 validators=[DataRequired(),
                                             Length(min=10, max=1024)])
    submit = SubmitField('Add Record')


class EditMedicalrecordForm(FlaskForm):
    """Create a form to search a patient"""
    diagnosis = TextAreaField('Diagnosis',
                              validators=[DataRequired(),
                                          Length(min=10, max=1024)])

    prescription = TextAreaField('Prescription',
                                 validators=[DataRequired(),
                                             Length(min=10, max=1024)])
    submit = SubmitField('Edit Record')
