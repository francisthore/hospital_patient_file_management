#!/usr/bin/python3
"""Front End Stuff"""
from routes.auth import auth
from routes.profile import user_profile
from routes.admin import admin
from routes.staff import staff_r
from models import storage
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from api.v1 import app as backend_app
import os
from dotenv import load_dotenv


load_dotenv()
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
APP_KEY = os.getenv('MAIN_APP_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
app.config['MAILGUN_API_KEY'] = MAILGUN_API_KEY
app.config['MAILGUN_DOMAIN'] = MAILGUN_DOMAIN
app.config['SESSION_TYPE'] = 'filesystem'
app.register_blueprint(auth)
app.register_blueprint(user_profile)
app.register_blueprint(admin)
app.register_blueprint(staff_r)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id):
    return storage.get('User', user_id)


@app.before_request
def link_session():
    """Links session cookies between the front end and API"""
    request.backend_app = backend_app


@app.errorhandler(403)
def handle_unauthorised(err):
    """Handles 403 Error"""
    return render_template('unauthorized.html')


@app.errorhandler(404)
def handle_not_found(err):
    """Handles 404 Error"""
    return render_template('not_found.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
