#!/usr/bin/python3
"""This defines a user model for authentication
purposes"""
import models
from models.base_model import BaseModel, Base
from flask_login import UserMixin
from flask import current_app
from sqlalchemy import Column, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer


class User(BaseModel, Base, UserMixin):
    """Class defining a user model"""
    __tablename__ = 'users'
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    verified = Column(Boolean, default=False)
    verification_token = Column(String(128))
    role = Column(String(10), default='user')

    def generate_verification_token(self, expires_sec='3600'):
        """Generates an email verification code"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_verification_token(token):
        """verifies a token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return models.storage.get(User, user_id)

    def set_password(self, password):
        """Creates a hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password against hashed password"""
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        """Returns true if user in authenticated"""
        return True

    @property
    def is_active(self):
        """Returns true if a user is active"""
        return True

    @property
    def is_anonymous(self):
        """Returns false for anonymous users"""
        return False

    def get_id(self):
        """Returns th user object id"""
        return str(self.id)
