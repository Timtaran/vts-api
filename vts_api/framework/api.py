import uuid

from aiohttp import ClientWebSocketResponse
from ujson import dumps

from vts_api.utils import merge_dicts
from vts_api.types.base import BaseRequest


class API:
    def __init__(self, required_kwargs: dict, websocket: ClientWebSocketResponse):
        self._required_kwargs = required_kwargs
        self._websocket = websocket

    async def send_request(
        self, request_data: BaseRequest, request_id: str | None = None
    ):
        if not request_id:
            request_id = str(uuid.uuid4())

        dt = dumps(
            merge_dicts(
                request_data.model_dump(by_alias=True),
                {
                    "messageType": request_data.__class__.__name__,
                    "requestID": request_id,
                },
                self._required_kwargs,
            )
        )

        await self._websocket.send_str(dt)
