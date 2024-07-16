from typing import Optional

from loguru import logger

from vts_api.types import Handler, APIError


class NotAnEventType(Exception):
    pass


class OnlyCoroutinesAllowed(Exception):
    pass


class APIErrorException(Exception):
    def __init__(self, error: APIError):
        self.error = error

        logger.debug(
            f"Server response an API Error with {error.data.errorID} code: {error.data.message}"
        )

    def __str__(self):
        return self.error.data.message


class MimicException(Exception):  # Created for `_handle_exception` method
    def __init__(self, exception: BaseException):
        self.exception = exception
