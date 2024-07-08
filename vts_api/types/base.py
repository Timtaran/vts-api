from typing import Optional

from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    api_name: Optional[str] = Field(None, alias="apiName")
    api_version: Optional[str] = Field(None, alias="apiVersion")
    message_type: str = Field(None, alias="messageType")
    request_id: Optional[str] = Field(None, alias="requestID")


class BaseResponse(BaseModel):
    api_name: str = Field(alias="apiName")
    api_version: str = Field(alias="apiVersion")
    timestamp: int = Field(alias="timestamp")
    message_type: str = Field(alias="messageType")
    request_id: str = Field(alias="requestID")
