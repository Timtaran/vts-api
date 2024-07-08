from pydantic import BaseModel

from .base import BaseResponse


class APIErrorData(BaseModel):
    errorID: int
    message: str


class APIError(BaseResponse):
    data: APIErrorData
