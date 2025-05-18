from flask import Blueprint

api = Blueprint('api', __name__)

from app.views.user import * 
from app.views.category import *
from app.views.record import *