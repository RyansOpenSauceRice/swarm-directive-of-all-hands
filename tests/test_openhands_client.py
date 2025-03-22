import pytest
import json
from core.openhands_client import OpenHandsClient, OpenHandsEndpoint
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_client():
    config = {
        "endpoints": [
            {
                "name": "test",
                "url": "ws://localhost:51090",
                "api_key": "test-key",
                "timeout": 30,
                "active": True
            }
        ],
        "default_timeout": 30,
        "max_retries": 3
    }
    return OpenHandsClient(config)

@pytest.mark.asyncio
async def test_send_command_success(mock_client):
    endpoint = mock_client.endpoints[0]
    mock_response = {"status": "success"}
    
    with patch('websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_ws = AsyncMock()
        mock_ws.recv.return_value = json.dumps(mock_response)
        mock_connect.return_value.__aenter__.return_value = mock_ws
        
        response = await mock_client.send_command(endpoint, "test")
        assert response == mock_response

@pytest.mark.asyncio
async def test_send_command_failure(mock_client):
    endpoint = mock_client.endpoints[0]
    
    with patch('websockets.connect', new_callable=AsyncMock) as mock_connect:
        mock_connect.side_effect = ConnectionError("Test error")
        
        with pytest.raises(ConnectionError):
            await mock_client.send_command(endpoint, "test")

def test_get_active_endpoints(mock_client):
    endpoints = mock_client.get_active_endpoints()
    assert len(endpoints) == 1
    assert endpoints[0].name == "test"