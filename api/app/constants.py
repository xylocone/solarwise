"""
File containing all the constants for the app
"""
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWD = os.environ.get('ADMIN_PASSWD')


TITLE = "Flask - backend"

STRINGS: dict[str, str] = {
    "user": {
        # Regarding authentication
        "login-success": "user logged in successfully, email: {}",
        "register-success": "user registered successfully, email: {}",
        
        "already-exists": "user already exists",
        "not-found": "user not found",
        "unauthorized": "password is incorrect"
    },
}