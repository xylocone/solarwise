from flask_login import UserMixin
from typing import Any

# Custom utilities
from . import get_uuid, now
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Text, nullable=False)

    # The timestamp columns
    created = db.Column(db.DateTime, default=now)

    @staticmethod
    def serialize_fields() -> list:
        return list(
            map(lambda f: {
                'name': f.name,
                'type': f.type,
                'primary_key': f.primary_key,
                'unique': f.unique,
                'nullable': f.nullable,
                'default': f.default,
                'field': f,
            }, [User.id, User.email, User.username, User.created])
        )

    @staticmethod
    def serialize(instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "email": instance.email,
            "username": instance.username,
            "created": instance.created,
        }

