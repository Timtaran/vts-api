from loguru import logger

from vts_api.types import AuthenticationResponse


class AuthenticationException(Exception):
    def __init__(self, response: AuthenticationResponse):
        self.response = response

        logger.debug(f"Error while authentication: {response.data.reason}")

    def __str__(self):
        return self.response.data.reason


class CriticalErrorException(Exception):
    def __init__(self, exception: BaseException, check_auth: bool):
        """
        Critical error exception
        :param exception:
        :param check_auth: Should connector check for authenticated listener state
        """

        self.exception = exception
        self.check_auth = check_auth
