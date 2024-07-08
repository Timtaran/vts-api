"""Main class for VTS API"""

import asyncio
from asyncio import AbstractEventLoop

import aiohttp

from typing import Optional
from loguru import logger

from .listener import Listener
from .api import API
from vts_api.utils import Icon
from vts_api.types import (
    AuthenticationTokenRequestData,
    AuthenticationTokenRequest,
    AuthenticationTokenResponse,
    AuthenticationRequest,
    EventTypes,
    AuthenticationRequestData,
    AuthenticationResponse,
)


class Connector:
    def __init__(
        self,
        websocket_ip: str = "ws://127.0.0.1:8001",
        plugin_name: str = "Unknown",
        plugin_developer: str = "Unknown",
        plugin_icon: Optional[Icon | str] = None,
    ):
        """
        ``VTubeStudio API`` Connector
        :param websocket_ip: IP of VTS websocket
        :param plugin_name: your plugin name
        :param plugin_developer: your plugin developer
        :param plugin_icon: icon of plugin, utils.Icon instance or bytes64 str.
        """

        logger.debug("Initializing API")
        logger.debug("Connecting to socket and creating listener")

        self.websocket_ip = websocket_ip
        self.plugin_name = plugin_name
        self.plugin_developer = plugin_developer

        self._loop = None

        if isinstance(plugin_icon, Icon):
            self.plugin_icon = plugin_icon.icon_data
        else:
            self.plugin_icon = plugin_icon

        self.listener = Listener(websocket=None)

    async def _after_listener_start(self):
        while not self.listener.listener_started:
            pass

    async def start_polling(self):
        # noinspection PyAttributeOutsideInit
        self._loop = asyncio.get_running_loop()
        self.listener.loop = self.loop

        self._register_events()
        await self._connect()

        await self._auth()
        await self.listener.start_listening()

    def run_polling(self):
        asyncio.run(self.start_polling())

    async def _connect(self):
        logger.debug("Connecting to websocket.")
        self.websocket = await aiohttp.ClientSession().ws_connect(url=self.websocket_ip)
        self.listener.update_websocket(websocket=self.websocket)
        self.api = API(
            websocket=self.websocket,
            required_kwargs={
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
            },
        )

    async def _auth(self):
        logger.debug("Sending token request.")
        await self.api.send_request(
            AuthenticationTokenRequest(
                data=AuthenticationTokenRequestData(
                    pluginName=self.plugin_name,
                    pluginDeveloper=self.plugin_developer,
                    pluginIcon=self.plugin_icon,
                )
            )
        )

    def _register_events(self):
        @self.listener.on_event(EventTypes.AuthenticationTokenResponse)
        async def on_token_response(response: AuthenticationTokenResponse):
            await self.api.send_request(
                AuthenticationRequest(
                    data=AuthenticationRequestData(
                        authenticationToken=response.data.authentication_token,
                        pluginName=self.plugin_name,
                        pluginDeveloper=self.plugin_developer,
                    )
                )
            )

        @self.listener.on_event(EventTypes.AuthenticationResponse, skippable=False)
        async def on_auth(response: AuthenticationResponse):
            if response.data.authenticated:
                logger.debug("Success authentication.")
            else:
                logger.error(f"Error while authentication: {response.data.reason}")

    @property
    def loop(self) -> AbstractEventLoop | None:
        if self._loop:
            return self._loop
        else:
            logger.error(
                "Don't use .loop until polling started. To create on_start event use ."
            )
            return None


class Tasks:
    def __init__(self):
        self.on_start = []
        self.on_connect = []
        self.on_shutdown = []
