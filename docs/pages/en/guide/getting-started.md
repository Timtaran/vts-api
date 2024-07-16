# VTS-API

`vts-api` - a strict-typing asynchronous framework for working with the VTubeStudio API.

## Preparing{#preparing}

First install the framework using command below:
```shell
pip install vts-api
```

Last version from GitHub
```shell
pip install -U https://github.com/Timtaran/vts-api/archive/refs/heads/master.zip
```

Development version from GitHub
```shell
pip install -U https://github.com/Timtaran/vts-api/archive/refs/heads/dev.zip
```

## Example usage{#example}

In this example, we process each new event that the server has sent us an authorization token.

```python
from vts_api import Connector, EventTypes 
from vts_api.types import AuthenticationTokenResponse

from loguru import logger

vts = Connector(
    websocket_ip="ws://127.0.0.1:8001",  # All params are optional
    plugin_name="Test Integration", 
    plugin_developer="Timtaran"
) 


@vts.listener.on_event(EventTypes.AuthenticationTokenResponse)  # Handler registration 
async def on_token_response(response: AuthenticationTokenResponse) -> None:
	logger.info(f'Server send authentication_token: {response.data.authentication_token}')

vts.run_polling()
```
