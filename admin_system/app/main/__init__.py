from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates') # Define template_folder

from app.main import routes # Import routes after blueprint
