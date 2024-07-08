from enum import Enum


class EventTypes(Enum):
    Any = "_ANY_EVENT_"
    AuthenticationResponse = "AuthenticationResponse"
    AuthenticationTokenResponse = "AuthenticationTokenResponse"
