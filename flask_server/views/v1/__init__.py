#!/usr/bin/python3
"""This module is used to manage our blueprints
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')
from flask_server.views.v1.user import *
