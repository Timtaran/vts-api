from .base import BaseRequest, BaseResponse
from .data import APIStateResponseData


class APIStateRequest(BaseRequest):
    pass


class APIStateResponse(BaseResponse):
    data: APIStateResponseData
