#!/usr/bin/python3
"""Module to handle my custom
decorators that will help with RBAC"""
from functools import wraps
from flask import abort
from flask_login import current_user
from models import storage
from models.user import User


def admin_required(func):
    """Checks if user is logged in and their role
    is admin"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


def staff_one_required(func):
    """Checks if user is logged in and their role
    is staff_one and above"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        yes = ['staff_one', 'staff_two', 'admin']
        if not current_user.is_authenticated or current_user.role not in yes:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


def staff_two_required(func):
    """Checks if user is logged in and their role
    is staff_two and above"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        yes = ['staff_two', 'admin']
        if not current_user.is_authenticated or current_user.role not in yes:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view
