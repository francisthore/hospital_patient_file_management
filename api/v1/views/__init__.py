#!/usr/bin/python3
"""Views init"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views:
    from api.v1.views.index import *
    from api.v1.views.patients import *
    from api.v1.views.staff import *
    from api.v1.views.users import *
    from api.v1.views.medical_records import *
