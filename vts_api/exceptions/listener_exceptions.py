from loguru import logger

from vts_api.types.error import APIError


class NotAnEventType(Exception):
    pass


class OnlyCoroutinesAllowed(Exception):
    pass


class APIErrorException(Exception):
    def __init__(self, error: APIError):
        self.error = error
        logger.debug(f"Server response an API Error. Data: {error.data}")

    def __str__(self):
        return self.error.data.message
