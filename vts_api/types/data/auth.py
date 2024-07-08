from typing import Optional

from pydantic import BaseModel, Field


class AuthenticationTokenRequestData(BaseModel):
    plugin_name: str = Field(alias="pluginName")
    plugin_developer: str = Field(alias="pluginDeveloper")
    plugin_icon: Optional[str] = Field(None, alias="pluginIcon")


class AuthenticationTokenResponseData(BaseModel):
    authentication_token: str = Field(alias="authenticationToken")


class AuthenticationRequestData(BaseModel):
    plugin_name: str = Field(alias="pluginName")
    plugin_developer: str = Field(alias="pluginDeveloper")
    authentication_token: str = Field(alias="authenticationToken")


class AuthenticationResponseData(BaseModel):
    authenticated: bool
    reason: str
