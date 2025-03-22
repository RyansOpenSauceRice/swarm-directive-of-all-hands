import json
import asyncio
import websockets
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class OpenHandsEndpoint:
    name: str
    url: str
    api_key: str
    timeout: int
    active: bool

class OpenHandsClient:
    def __init__(self, config: Dict[str, Any]):
        self.endpoints = [
            OpenHandsEndpoint(**endpoint)
            for endpoint in config.get('endpoints', [])
        ]
        self.default_timeout = config.get('default_timeout', 30)
        self.max_retries = config.get('max_retries', 3)
        
    async def send_command(self, endpoint: OpenHandsEndpoint, command: str, 
                         params: Optional[Dict] = None) -> Dict:
        if not endpoint.active:
            raise ConnectionError("Endpoint is not active")
            
        params = params or {}
        payload = {
            "command": command,
            "params": params,
            "api_key": endpoint.api_key
        }
        
        for attempt in range(self.max_retries):
            try:
                async with websockets.connect(
                    endpoint.url,
                    timeout=self.default_timeout
                ) as websocket:
                    await websocket.send(json.dumps(payload))
                    response = await websocket.recv()
                    return json.loads(response)
            except (websockets.exceptions.ConnectionClosed, 
                   asyncio.TimeoutError) as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(
                        f"Failed to connect after {self.max_retries} attempts"
                    ) from e
                await asyncio.sleep(1)
                
    def get_active_endpoints(self) -> list[OpenHandsEndpoint]:
        return [e for e in self.endpoints if e.active]
        
    def add_endpoint(self, endpoint: Dict[str, Any]):
        self.endpoints.append(OpenHandsEndpoint(**endpoint))
        
    def remove_endpoint(self, endpoint_name: str):
        self.endpoints = [e for e in self.endpoints if e.name != endpoint_name]