#!/usr/bin/python3
"""Module to handle profile routes"""
from flask import (Blueprint,
                   render_template,
                   flash, redirect, url_for, request)
from flask_login import login_required, current_user
import requests


user_profile = Blueprint('user_profile', __name__)


@user_profile.route('/profile', methods=['GET'], strict_slashes=False)
@login_required
def profile():
    """User profile"""
    id = current_user.id
    session_cookies = request.cookies
    url = 'http://localhost:5001/api/v1/staff/{}'.format(id)
    with requests.get(url, cookies=session_cookies) as response:
        staff = response.json()
        if response.status_code == 404:
            flash('Member not found, register instead', 'danger')
            return redirect(url_for('auth.register_staff'))
    return render_template('profile.html', current_user=current_user,
                           staff=staff)
