#!/usr/bin/python3
"""Handles API calls for the user model"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from markupsafe import escape
from models.user import User


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves user's details"""
    user_id = escape(user_id)
    user = storage.get_by_user_id(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all users"""
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users), 200


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
    print('Deleting user')
    user_id = escape(user_id)
    user = storage.get_by_user_id(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user"""
    data = request.get_json()
    if not data:
        print('No JSON received')
        abort(400, 'Not a JSON')
    if 'username' not in data:
        abort(400, 'Missing username')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    new_user.verification_token = new_user.generate_verification_token()
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a user"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = escape(user_id)
    user = storage.get_by_user_id(User, user_id)
    if not user:
        abort(404)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password_hash' in data:
        user.password_hash = data['password_hash']
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<string:user_id>/staff', methods=['GET'],
                 strict_slashes=False)
def get_user_staff(user_id):
    """Retrieves all staff associated with a user"""
    user_id = escape(user_id)
    user = storage.get_by_user_id(User, user_id)
    if not user:
        abort(404)
    staff = user.staff
    staff = [staff.to_dict() for staff in staff]
    return jsonify(staff), 200
