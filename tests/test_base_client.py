import pytest
import aiohttp
from src.coingecko_api.base_client import CoinGeckoBaseClient, BaseAPIConfig

@pytest.mark.asyncio
async def test_base_client_initialization():
    """Test base client initialization."""
    async with CoinGeckoBaseClient() as client:
        assert client is not None

@pytest.mark.asyncio
async def test_base_client_config():
    """Test client configuration."""
    config = BaseAPIConfig(base_url="https://test.api.com", timeout=5, retries=2)
    client = CoinGeckoBaseClient(config)
    assert client._config.base_url == "https://test.api.com"
    assert client._config.timeout == 5
    assert client._config.retries == 2

@pytest.mark.skip(reason="Requires actual API access")
@pytest.mark.asyncio
async def test_base_client_request():
    """Test request method (skipped for now)."""
    async with CoinGeckoBaseClient() as client:
        # Simulate a request
        pass