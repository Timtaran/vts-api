from enum import Enum

from .auth import AuthenticationResponse, AuthenticationTokenResponse
from .error import APIError


class EventTypes(Enum):
    Any = "_ANY_EVENT_"
    AuthenticationResponse = AuthenticationResponse.__name__
    AuthenticationTokenResponse = AuthenticationTokenResponse.__name__
    APIError = APIError.__name__
