from flask_login import UserMixin

# Custom utilities
from . import get_uuid, now
from . import db

# New model for the admin access
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(345), unique=True)
    password = db.Column(db.String(30), nullable=False)
    
    # The timestamp columns
    created = db.Column(db.DateTime, default=now)



