import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from app.services.providers.mempool_provider import MempoolSpaceProvider
from app.services.providers.demo_provider import DemoDataProvider
from app.services.providers.factory import get_blockchain_provider

@pytest.mark.asyncio
async def test_mempool_provider_valid_address_success():
    provider = MempoolSpaceProvider(max_retries=0)
    mock_data = {
        "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "chain_stats": {"tx_count": 10, "funded_txo_sum": 50000000}
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        result = await provider.get_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        assert result["address"] == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        assert result["source"] == "Live Mempool.space API"

@pytest.mark.asyncio
async def test_mempool_provider_invalid_address_validation():
    provider = MempoolSpaceProvider()
    with pytest.raises(HTTPException) as exc_info:
        await provider.get_address("invalid_btc_address_123")
    assert exc_info.value.status_code == 400
    assert "Invalid Bitcoin address format" in exc_info.value.detail

@pytest.mark.asyncio
async def test_mempool_provider_invalid_txid_validation():
    provider = MempoolSpaceProvider()
    with pytest.raises(HTTPException) as exc_info:
        await provider.get_transaction("short_txid")
    assert exc_info.value.status_code == 400
    assert "Invalid Bitcoin transaction ID format" in exc_info.value.detail

@pytest.mark.asyncio
async def test_mempool_provider_timeout_handling():
    provider = MempoolSpaceProvider(timeout_seconds=0.1, max_retries=0)
    with patch("httpx.AsyncClient.get", side_effect=httpx.TimeoutException("Timeout")):
        with pytest.raises(HTTPException) as exc_info:
            await provider.get_address("bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0")
        assert exc_info.value.status_code == 504
        assert "timed out" in exc_info.value.detail

@pytest.mark.asyncio
async def test_mempool_provider_429_rate_limit_handling():
    provider = MempoolSpaceProvider(max_retries=0)
    mock_response = MagicMock()
    mock_response.status_code = 429

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        with pytest.raises(HTTPException) as exc_info:
            await provider.get_address("bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0")
        assert exc_info.value.status_code == 429
        assert "rate limit reached" in exc_info.value.detail

def test_provider_factory_selection():
    demo_p = get_blockchain_provider(force_live=False)
    assert isinstance(demo_p, DemoDataProvider)

    live_p = get_blockchain_provider(force_live=True)
    assert isinstance(live_p, MempoolSpaceProvider)
