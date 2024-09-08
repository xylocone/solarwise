"""
Initialize Flask application and register blueprints for each set of routes:
"""

from flask import Flask

# Custom modules
from config import ApplicationConfig

# Import the extensions
from .extensions import bcrypt, db, migrate

# Create the app instance
app = Flask(__name__)

# Set the configurations from external object
app.config.from_object(ApplicationConfig)

# Initialize extensions
bcrypt.init_app(app)
# Initialize the Database
db.init_app(app)

with app.app_context():
    db.create_all()

# Initialize the migrator
migrate.init_app(app, db)

# Import and register blueprints
from .routes.admin import admin_bp
from .routes.data import data_bp

# from .routes.<TODO: endpoint route here> import auth_bp

# Register blueprints
app.register_blueprint(admin_bp, url_prefix="/_/admin")

# The APIS for db access
app.register_blueprint(data_bp, url_prefix="/api/data")
