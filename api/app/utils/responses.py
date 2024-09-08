from logger import logger
import json

"""
Basic response from the API
"""


class Response:
    def __init__(self, msg: str, code: int, payload=None):
        self.msg = msg
        self.code = code
        self.payload = payload

        try:
            self.payload = json.loads(payload)
        except Exception as e:
            self.payload = payload

    @property
    def response(self):
        return {
            "msg": self.msg,
            "raw_msg": self.msg,
            "code": self.code,
            "payload": self.payload,
        }, self.code


class Success(Response):
    def __init__(self, msg: str, payload=None):
        super().__init__(msg, code=200, payload=payload)


"""
Definition of some exceptions that can be thrown in the app
"""


class APIBaseException(Response):
    def __init__(self, msg: str, code: int, payload=None):
        super().__init__(msg, code, payload)
        self.prefix = "Error: "
        # Log an error
        logger.error(msg=self.msg)

    @property
    def response(self):
        resp, _ = super().response
        resp["msg"] = self.prefix + self.msg
        return resp, self.code


class BadRequestException(APIBaseException):
    def __init__(self, msg: str):
        super().__init__(msg, code=400)
        self.prefix = "Bad Request: "


class ConflictException(APIBaseException):
    def __init__(self, msg: str):
        super().__init__(msg, code=409)
        self.prefix = "Conflict: "


class NotFoundException(APIBaseException):
    def __init__(self, msg: str):
        super().__init__(msg, code=404)
        self.prefix = "Not found: "


class UnauthorizedException(APIBaseException):
    def __init__(self, msg: str):
        super().__init__(msg, code=404)
        self.prefix = "Unauthorized: "


class ServiceUnavailableException(APIBaseException):
    def __init__(self, msg: str):
        super().__init__(msg, code=503)
        self.prefix = "Service Unavailable: "
