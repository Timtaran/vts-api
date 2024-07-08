from enum import Enum

from .auth import AuthenticationResponse, AuthenticationTokenResponse


class EventTypes(Enum):
    Any = "_ANY_EVENT_"
    AuthenticationResponse = AuthenticationResponse.__name__
    AuthenticationTokenResponse = AuthenticationTokenResponse.__name__
