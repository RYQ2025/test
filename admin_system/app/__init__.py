from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Will be defined in an auth blueprint
login_manager.login_message_category = 'info'

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app import routes, models
