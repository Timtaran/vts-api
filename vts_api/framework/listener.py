import asyncio
from asyncio import AbstractEventLoop

from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType, ClientSession
from ujson import loads
from loguru import logger

from vts_api.exceptions import (
    NotAnEventType,
    OnlyCoroutinesAllowed,
    APIErrorException,
    MimicException,
    CriticalErrorException,
)
from vts_api.types.error import APIError
from vts_api.utils import class_by_event_name
from vts_api.types import class_by_event_name_list, EventTypes, Handler


class SkipHandler(Exception):  # raise this to skip current handler
    pass


class Listener:
    def __init__(
        self, websocket: ClientWebSocketResponse | None, session: ClientSession | None
    ):
        """
        Event listener.
        :param websocket: websocket
        """
        self.loop: AbstractEventLoop | None = None
        self._websocket = websocket
        self._session = session
        self._custom_events = {}
        self._handlers: dict[
            str, list[Handler]
        ] = {}  # List of listeners in format {"messageType" : [(SKIPPABLE, coroutine1), ...]}

        self.listener_started = False
        self._auth = False  # Is api authorized

    async def start_listening(self):
        if self.listener_started:
            logger.debug("Listener already started")
            return

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

    async def stop_listening(self):
        self.listener_started = False
        await self._session.close()
        await self._websocket.close()

    @staticmethod
    def _handle_exception(exception: BaseException):
        if isinstance(exception, MimicException):
            if isinstance(exception.exception, APIErrorException):
                if (
                    exception.exception.error.data.errorID
                    in [  # Possible error codes: https://github.com/DenchiSoft/VTubeStudio/blob/master/Files/ErrorID.cs
                        51,
                        52,
                        53,
                        54,
                        55,
                    ]
                ):
                    raise CriticalErrorException(exception.exception, True)

    @logger.catch(onerror=_handle_exception)  # //todo fix really big stack trace
    async def _on_message(self, data):
        if (
            data["messageType"] in self._handlers or "_ANY_EVENT_" in self._handlers
        ):  # Check if event registered
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

                typed_data = event_class.model_validate(data)

                for handler in all_handlers:  # Calling unskippable handlers first
                    if not handler.skippable:
                        await self.loop.create_task(handler.function(typed_data))
                        all_handlers.remove(handler)

                for handler in all_handlers:
                    try:
                        await self.loop.create_task(handler.function(typed_data))
                    except SkipHandler:
                        pass
                    except Exception as ex:
                        logger.error(
                            f"Exception caught while calling the {handler.function.__name__}. Skipping handler. Exception: {ex}"
                        )
                    else:
                        break

        if data["messageType"] == "APIError":
            raise MimicException(APIErrorException(APIError.model_validate(data)))

    def add_handler(
        self, event_type: EventTypes, function, skippable: bool = True
    ) -> None:
        """
        Adds a new handler
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
        :param event_type: event_type (message_type)
        :param skippable: defines can handler be skipped
        :return decorator:
        """

        def decorator(func):
            self.add_handler(event_type, func, skippable)

            async def f():
                func()

            return f

        return decorator

    def update_websocket(
        self, session: ClientSession, websocket: ClientWebSocketResponse
    ):
        self._websocket = websocket
        self._session = session

    @property
    def auth(self) -> bool:
        """
        Is listener authorized
        :return bool:
        """
        return self._auth
