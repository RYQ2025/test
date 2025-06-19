from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates') # Define template_folder if specific to blueprint

from app.auth import routes # Import routes after blueprint creation
