from app.utils.responses import APIBaseException
from email_validator import validate_email as ve, EmailNotValidError
from logger import logger
from typing import Dict


def get_or_none(dict_obj: Dict, key, default=None):
    """
    Checks if the given key is valid for the dict object
    returns The value if found, else None
    """
    try:
        return dict_obj[key]
    except KeyError:
        return default
    except Exception as e:
        logger.error(
            f"error while parsing value for dict object: {dict_obj.__str__()}, key: {key}"
        )
        return None


def validate_none(exception_cls: APIBaseException, **kwargs):
    """
    Checks is any of the fields given is none
    """
    for field in kwargs:
        try:
            assert kwargs.get(field)
        except AssertionError:
            return exception_cls(msg=f"{field} is required", code=400)

    return None


def validate_email(exception_cls: APIBaseException, email: str):
    """
    Checks if the given email address is valid
    """
    try:
        ve(email, check_deliverability=True)
    except EmailNotValidError:
        return exception_cls(msg=f"{email} is invalid", code=400)

    return None
