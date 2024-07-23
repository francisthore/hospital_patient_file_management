#!/usr/bin/python3
"""Front End Stuff"""
from routes.auth import auth
from routes.profile import user_profile
from routes.admin import admin
from routes.staff import staff_r
from models import storage
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from flask.wrappers import Response
import os
from api.v1.api import api
from dotenv import load_dotenv


load_dotenv()
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
APP_KEY = os.getenv('MAIN_APP_KEY')
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
app.config['MAILGUN_API_KEY'] = MAILGUN_API_KEY
app.config['MAILGUN_DOMAIN'] = MAILGUN_DOMAIN
app.config['SESSION_TYPE'] = 'filesystem'
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
CORS(app)
CSRFProtect(app)
app.register_blueprint(auth)
app.register_blueprint(user_profile)
app.register_blueprint(admin)
app.register_blueprint(staff_r)
app.register_blueprint(api)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return storage.get('User', user_id)


@app.errorhandler(403)
def handle_unauthorised(err):
    """Handles 403 Error"""
    return render_template('unauthorized.html'), 403


@app.after_request
def add_csrf_cookie(response: Response):
    if response.status_code in range(200, 400) and not response.direct_passthrough:
        response.set_cookie("csrftoken", generate_csrf(), secure=True)
    return response


@app.errorhandler(404)
def handle_not_found(err):
    """Handles 404 Error"""
    return render_template('not_found.html'), 404


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    """Index of app"""
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
