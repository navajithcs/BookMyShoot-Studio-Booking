from flask import Blueprint

photographer_bp = Blueprint('photographer', __name__, template_folder='templates')

from . import routes
