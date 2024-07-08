from pydantic import BaseModel


class APIStateResponseData(BaseModel):
    active: bool
    vtube_studio_version: str
    current_session_authenticated: bool
