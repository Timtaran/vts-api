# VTS-API

Типизированный python фреймворк для работы с VTube Studio.

## Подготовка

Для начала работы установите фреймворк следующей командой:
```shell
pip install vts-api
```

## Пример использования

В этом примере мы обрабатываем каждый новый ивент о том, что сервер отправил нам токен авторизации.

```python
from vts_api import Connector, EventTypes 
from vts_api.types import AuthenticationTokenResponse

from loguru import logger

vts = Connector(websocket_ip="ws://127.0.0.1:8001",  # Все параметры необязательны
                plugin_name="Test Integration", 
                plugin_developer="Timtaran")


@vts.listener.on_event(EventTypes.AuthenticationTokenResponse)  # Handler registration 
async def on_token_response(response: AuthenticationTokenResponse) -> None:
	logger.info(f'Server send authentication_token: {response.data.authentication_token}')

vts.run_polling()
```
