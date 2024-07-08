import asyncio
from asyncio import AbstractEventLoop

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType
from ujson import loads
from loguru import logger

from vts_api.exceptions import NotAnEventType, OnlyCoroutinesAllowed, APIErrorException
from vts_api.types.error import APIError
from vts_api.utils import class_by_event_name
from vts_api.types import class_by_event_name_list, EventTypes, Handler


class SkipHandler(Exception):  # raise this to skip current handler
    pass


class Listener:
    def __init__(self, websocket: ClientWebSocketResponse | None):
        """
        Event listener.
        :param websocket: websocket
        """
        self.loop: AbstractEventLoop | None = None
        self._websocket = websocket
        self._custom_events = {}
        self._handlers: dict[
            str, list[Handler]
        ] = {}  # List of listeners in format {"messageType" : [(SKIPPABLE, coroutine1), ...]}

        self.listener_started = False

    async def start_listening(self):
        self.listener_started = True

        async for msg in self._websocket:
            msg: WSMessage
            data = loads(msg.data)

            if msg.type == WSMsgType.TEXT:
                logger.debug(f"Got a new message from server: {data}")
                # noinspection PyUnresolvedReferences
                await self._on_message(data)

            elif msg.type == WSMsgType.ERROR:
                logger.debug(f"Got an error from websocket: {msg}")
                break

    @logger.catch()
    async def _on_message(self, data):
        if data["messageType"] == "APIError":
            error_data = APIError.model_validate(data)
            raise APIErrorException(error_data)

        elif data["messageType"] in self._handlers or "_ANY_EVENT_" in self._handlers:
            if data["messageType"] in class_by_event_name_list:
                event_class = class_by_event_name(data["messageType"])

            elif data["messageType"] in self._custom_events:
                event_class = self._custom_events[data["messageType"]]

            else:
                event_class = None
                logger.error(f'Unknown event type {data["messageType"]}.')

            if event_class:
                all_handlers = (
                    self._handlers[data["messageType"]]
                    + [
                        self._handlers["_ANY_EVENT_"]
                        if EventTypes.Any in self._handlers
                        else []
                    ][0]
                )

                for handler in all_handlers:  # Calling unskippable handlers first
                    if not handler.skippable:
                        await self.loop.create_task(
                            handler.function(event_class.model_validate(data))
                        )
                        all_handlers.remove(handler)

                for handler in all_handlers:
                    try:
                        await self.loop.create_task(
                            handler.function(event_class.model_validate(data))
                        )
                    except SkipHandler:
                        pass
                    except Exception as ex:
                        logger.error(
                            f"Exception caught while calling the {handler.function.__name__}. Skipping handler. Exception: {ex}"
                        )
                    else:
                        break

    def add_listener(
        self, event_type: EventTypes, function, skippable: bool = True
    ) -> None:
        """
        Adds a new listener
        :param event_type: event_type (message_type)
        :param function: function, what is going to be called on event
        :param skippable: defines can handler be skipped
        :return None: function doesn't return anything
        """
        if not isinstance(event_type, EventTypes):
            raise NotAnEventType("Only EventTypes are allowed as event_type")

        if not asyncio.iscoroutinefunction(function):
            raise OnlyCoroutinesAllowed(
                "Only async coroutines are allowed to be added to the listener"
            )

        event_name = event_type.value

        if event_name not in self._handlers:
            self._handlers[event_name] = []

        self._handlers[event_name].append(
            Handler(skippable=skippable, function=function)
        )

    def on_event(self, event_type: EventTypes, skippable: bool = True):
        """
        Returns
        :param event_type: event_type (message_type)
        :param skippable: defines can handler be skipped
        :return decorator:
        """

        def decorator(func):
            self.add_listener(event_type, func, skippable)

            async def f():
                func()

            return f

        return decorator

    def update_websocket(self, websocket: ClientWebSocketResponse):
        self._websocket = websocket
