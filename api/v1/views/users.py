#!/usr/bin/python3
""" New view for User model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


