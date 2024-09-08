from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


# To export to the app
from app.models import db

# Passwords and cryptography
bcrypt = Bcrypt()
# For database management
migrate = Migrate()
